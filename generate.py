import argparse
import os

import cv2
import numpy as np
import torch
import sys

from .utils.imgops import crop_seamless, esrgan_launcher_split_merge
from .utils.architecture.architecture import RRDB_Net
from .absolute_path import absolute_path

class GenerateMaterialMap:

    def __init__(self):

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--input', default=absolute_path("input"), help='Input folder')
        self.parser.add_argument('--output', default=absolute_path("output"), help='Output folder')
        self.parser.add_argument('--reverse', help='Reverse Order', action="store_true")
        self.parser.add_argument('--tile_size', default=512,
                            help='Tile size for splitting', type=int)
        self.parser.add_argument('--seamless', action='store_true',
                            help='Seamless upscaling')
        self.parser.add_argument('--mirror', action='store_true',
                            help='Mirrored seamless upscaling')
        self.parser.add_argument('--replicate', action='store_true',
                            help='Replicate edge pixels for padding')
        self.parser.add_argument('--cpu', action='store_true',
                            help='Use CPU instead of CUDA')
        self.parser.add_argument('--ishiiruka', action='store_true',
                            help='Save textures in the format used in Ishiiruka Dolphin material map texture packs')
        self.parser.add_argument('--ishiiruka_texture_encoder', action='store_true',
                            help='Save textures in the format used by Ishiiruka Dolphin\'s Texture Encoder tool')
        self.args = self.parser.parse_args()

        if not os.path.exists(self.args.input):
            print('Error: Folder [{:s}] does not exist.'.format(self.args.input))
            sys.exit(1)
        elif os.path.isfile(self.args.input):
            print('Error: Folder [{:s}] is a file.'.format(self.args.input))
            sys.exit(1)
        elif os.path.isfile(self.args.output):
            print('Error: Folder [{:s}] is a file.'.format(self.args.output))
            sys.exit(1)
        elif not os.path.exists(self.args.output):
            os.mkdir(self.args.output)

        isCudaAvailable = torch.cuda.is_available()
        if not isCudaAvailable:
            print("Warning: Couldn't find available CUDA devices, using cpu instead")

        self.device = torch.device('cpu' if self.args.cpu or not isCudaAvailable else 'cuda')

        self.input_folder = os.path.normpath(self.args.input)
        self.output_folder = os.path.normpath(self.args.output)

        self.NORMAL_MAP_MODEL = absolute_path('utils/models/1x_NormalMapGenerator-CX-Lite_200000_G.pth')
        self.OTHER_MAP_MODEL = absolute_path('utils/models/1x_FrankenMapGenerator-CX-Lite_215000_G.pth')

    def process(self, img, model):
        img = img * 1. / np.iinfo(img.dtype).max
        img = img[:, :, [2, 1, 0]]
        img = torch.from_numpy(np.transpose(img, (2, 0, 1))).float()
        img_LR = img.unsqueeze(0)
        img_LR = img_LR.to(self.device)

        output = model(img_LR).data.squeeze(
            0).float().cpu().clamp_(0, 1).numpy()
        output = output[[2, 1, 0], :, :]
        output = np.transpose(output, (1, 2, 0))
        output = (output * 255.).round()
        return output

    def load_model(self, model_path):
        global device
        state_dict = torch.load(model_path)
        model = RRDB_Net(3, 3, 32, 12, gc=32, upscale=1, norm_type=None, act_type='leakyrelu',
                                mode='CNA', res_scale=1, upsample_mode='upconv')
        model.load_state_dict(state_dict, strict=True)
        del state_dict
        model.eval()
        for k, v in model.named_parameters():
            v.requires_grad = False
        return model.to(self.device)

    def start(self):
        images=[]
        for root, _, files in os.walk(self.input_folder):
            for file in sorted(files, reverse=self.args.reverse):
                if file.split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tga']:
                    images.append(os.path.join(root, file))
        models = [
            # NORMAL MAP
            self.load_model(self.NORMAL_MAP_MODEL), 
            # ROUGHNESS/DISPLACEMENT MAPS
            self.load_model(self.OTHER_MAP_MODEL)
            ]
        for idx, path in enumerate(images, 1):
            base = os.path.splitext(os.path.relpath(path, self.input_folder))[0]
            output_dir = os.path.dirname(os.path.join(self.output_folder, base))
            os.makedirs(output_dir, exist_ok=True)
            print(idx, base)
            # read image
            try: 
                img = cv2.imread(path, cv2.cv2.IMREAD_COLOR)
            except:
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                
            # Seamless modes
            if self.args.seamless:
                img = cv2.copyMakeBorder(img, 16, 16, 16, 16, cv2.BORDER_WRAP)
            elif self.args.mirror:
                img = cv2.copyMakeBorder(img, 16, 16, 16, 16, cv2.BORDER_REFLECT_101)
            elif self.args.replicate:
                img = cv2.copyMakeBorder(img, 16, 16, 16, 16, cv2.BORDER_REPLICATE)

            img_height, img_width = img.shape[:2]

            # Whether or not to perform the split/merge action
            do_split = img_height > self.args.tile_size or img_width > self.args.tile_size

            if do_split:
                rlts = esrgan_launcher_split_merge(img, self.process, models, scale_factor=1, tile_size=self.args.tile_size)
            else:
                rlts = [self.process(img, model) for model in models]

            if self.args.seamless or self.args.mirror or self.args.replicate:
                rlts = [crop_seamless(rlt) for rlt in rlts]

            normal_map = rlts[0]
            roughness = rlts[1][:, :, 1]
            displacement = rlts[1][:, :, 0]

            if self.args.ishiiruka_texture_encoder:
                r = 255 - roughness
                g = normal_map[:, :, 1]
                b = displacement
                a = normal_map[:, :, 2]
                output = cv2.merge((b, g, r, a))
                cv2.imwrite(os.path.join(self.output_folder, '{:s}.mat.png'.format(base)), output)
            else:
                normal_name = '{:s}.nrm.png'.format(base) if self.args.ishiiruka else '{:s}_Normal.png'.format(base)
                cv2.imwrite(os.path.join(self.output_folder, normal_name), normal_map)

                rough_name = '{:s}.spec.png'.format(base) if self.args.ishiiruka else '{:s}_Roughness.png'.format(base)
                rough_img = 255 - roughness if self.args.ishiiruka else roughness
                cv2.imwrite(os.path.join(self.output_folder, rough_name), rough_img)

                displ_name = '{:s}.bump.png'.format(base) if self.args.ishiiruka else '{:s}_Displacement.png'.format(base)
                cv2.imwrite(os.path.join(self.output_folder, displ_name), displacement)
