import open_clip
import torch
from PIL import Image

model, _, transform = open_clip.create_model_and_transforms(
  model_name="coca_ViT-L-14",
  pretrained="mscoco_finetuned_laion2B-s13B-b90k"
)

im = Image.open(r"C:\Users\andre\Desktop\Canopy Tower\Gamboa_RDCbottom_comerLicaon_2024-11-14\2024-11-14\patches\comerLicaón_2024_11_14__19_02_21_HDR0_0_Mothbot_best.pt.jpg").convert("RGB")
im = transform(im).unsqueeze(0)

with torch.no_grad(), torch.amp.autocast('cuda'):
  generated = model.generate(im)

print(open_clip.decode(generated[0]).split("<end_of_text>")[0].replace("<start_of_text>", ""))