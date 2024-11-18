import torch
from torchvision.transforms.functional import to_tensor, to_pil_image
from PIL import Image

from src.modules.RRDBNet import RRDBNet

def load_model(model_path):
    """
    Load the ESRGAN model and prepare it for inference.

    Args:
        model_path (str): Path to the pre-trained ESRGAN model file (.pth).

    Returns:
        model: Loaded PyTorch model.
        device: The device (CPU/GPU) the model is loaded on.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Load state_dict from the .pth file
    state_dict = torch.load(model_path, map_location=device)
    
    # Initialize the model architecture (ensure this matches the .pth file)
    model = RRDBNet()  # Replace with the appropriate architecture

    # Try loading the state_dict with strict=False
    try:
        model.load_state_dict(state_dict, strict=False)
    except RuntimeError as e:
        print(f"State_dict mismatch: {e}")
        raise e

    model = model.to(device)
    model.eval()
    return model, device

def get_upscale_image(model, device, img_path):
    """
    Upscale an image using the ESRGAN model.
    
    Args:
        model: The loaded ESRGAN model.
        device: The device (CPU/GPU) for inference.
        img_path (str): Path to the input image file.
        
    Returns:
        PIL.Image: The upscaled image.
    """
    # Load and preprocess the image
    img = Image.open(img_path).convert("RGB")
    input_tensor = to_tensor(img).unsqueeze(0).to(device)  # Add batch dimension and move to GPU/CPU

    # Perform upscaling
    with torch.no_grad():
        output_tensor = model(input_tensor)

    # Convert back to PIL Image
    upscaled_img = to_pil_image(output_tensor.squeeze(0).cpu().clamp(0, 1))
    return upscaled_img
