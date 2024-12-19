# 创建一个 user-study 前端界面，界面中有 6 个图像框，其中 1 个图像框位于上侧，5 个图像框位于下侧
# 上册的 1 个图像来源于链接 http://10.133.4.94:8000/images?group=input&id=00690
# 下侧的 5 个图像框均可点击，点击后会显示"是否确认"的窗口，每个图像 i 都来源于链接 http://10.133.4.94:8000/images?group=output_i&id=00690
# 选择"确认"后，会将 i 对应的图像的 id 和 group 发送给后端，接着会将所有图像替换为 id 为 00691 的图像，并显示到前端界面上

import gradio as gr
import requests
from server import url
from PIL import Image
from io import BytesIO

# 上侧图像的链接

# 下侧图像的链接
outputs = ["FourLLIE", "LightenDiffusion", "LLFormer", "MIRNet", "RetinexFormer"]
ids = ["00690", "00691", "00692", "00693", "00694"]

def load_image(image_url):
    try:
        # 从 URL 加载图像
        response = requests.get(image_url)
        response.raise_for_status()  # 检查请求是否成功

        # 将图像转换为 PIL 格式
        image = Image.open(BytesIO(response.content))
        print(f"成功加载图像: {image_url}")
        return image
    except Exception as e:
        return f"无法加载图像: {e}"

# 创建 Gradio 界面
def create_user_study_interface():
    def update_images(index):
        input_image_url = f"{url}/images?group=input&id={id}"
        output_image_url = [f"{url}/images?group={outputs[i]}&id={id}" for i in range(len(outputs))]
        urls = [input_image_url] + output_image_url
        images = [input_image] + output_images

    with gr.Blocks() as demo:
        gr.Markdown("### User Study")

        id = ids[0]
        input_image_url = f"{url}/images?group=input&id={id}"
        output_image_url = [f"{url}/images?group={outputs[i]}&id={id}" for i in range(len(outputs))]

        # 上侧的图像框
        with gr.Row():
            input_image = gr.Image(label="输入图像", value=load_image(input_image_url))

        # 下侧的图像框
        output_images = []
        with gr.Column(scale=len(outputs)):
            for i in range(len(outputs)):
                output_image = gr.Image(label=f"输出图像 {i + 1}", value=load_image(output_image_url[i]))
                output_images.append(output_image)

                # 添加点击事件
                def confirm(index=i):
                    return gr.Ask("是否确认?", lambda x: update_images(index) if x else None)

                gr.Button("确认", elem_id=f"confirm_button_{i}").click(confirm)

        # 更新图像
        urls = [input_image_url] + output_image_url
        images = [input_image] + output_images
        gr.Button("更新图像").click(lambda: [image.set_image(load_image(url)) for image, url in zip(images, urls)])

    return demo


interface = create_user_study_interface()
interface.launch(share=True)
