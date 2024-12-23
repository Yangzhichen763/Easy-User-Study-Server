/**
 * 实现图片点击放大、拖拽、滚轴滚动焦点缩放功能，相关参数、函数声明
 * 代码来源：https://blog.csdn.net/qq_58441775/article/details/131963598
 */
let imgWidth, imgHeight; // 图片点击放大初始尺寸参数
let maxZoom = 4; //最大缩放倍数
let minZoom = 0.5; // 最小缩放倍数
let initScale = 1; //滚动缩放初始倍数，并不是图片点击放大的倍数
let isPointerdown = false; //鼠标按下的标识
//记录鼠标按下坐标和按下移动时坐标
let lastPointermove = {
    x: 0,
    y: 0,
};
//移动过程从上一个坐标到下一个坐标之间的差值
let diff = {
    x: 0,
    y: 0,
};
//图片放大后左上角的坐标，主要结合diff参数用于鼠标焦点缩放时图片偏移坐标
let x = 0;
let y = 0;

let imageViewer;
// 在 img Element 上绑定点击图像浏览事件
// 前提是要有 id 为 imageViewer 的 img Element
function addImageViewerListener(listenerType, allImages) {
    imageViewer = document.getElementById("imageViewer")
    allImages.forEach((imageElement) => {
        imageElement.addEventListener(listenerType, (e) => {
            e.preventDefault();

            const imageElement = e.target;
            imageViewer.style.transform = "scale(1)";
            //图片放大展示函数调用
            setupImageViewer(imageElement);
            // 监听鼠标滚动事件
            window.addEventListener("wheel", handleStopWheel, {
                passive: false,
            });
            // 拖转事件调用
            imgDrag();
        });
    });
}

function setupImageViewer(imageElement) {
    let src = imageElement.getAttribute("src");
    imageViewer.setAttribute("src", src);

    // 设置尺寸和调整比例
    let windowW = document.documentElement.clientWidth;
    let windowH = document.documentElement.clientHeight;
    let realWidth = imageViewer.naturalWidth; //获取图片的原始宽度
    let realHeight = imageViewer.naturalHeight; //获取图片的原始高度
    let outsideScale = 0.8;
    let belowScale = 1.4;
    let realRatio = realWidth / realHeight;
    let windowRatio = windowW / windowH;

    // 图片的真实尺寸大于屏幕尺寸则使用屏幕尺寸，如果小于屏幕尺寸就使用自己本身的尺寸；并根据大于或者小于的比例对图片的尺寸进一步调整
    if (realRatio >= windowRatio) {
        if (realWidth > windowW) {
            imgWidth = windowH * outsideScale;
            imgHeight = (imgWidth / realWidth) * realHeight;
        } else {
            if (realWidth * belowScale < windowW) {
                imgWidth = realWidth * (belowScale - 0.2);
                imgHeight = (imgWidth / realWidth) * realHeight;
            } else {
                imgWidth = realWidth;
                imgHeight = realHeight;
            }
        }
    }
    else {
        if (realHeight > windowH) {
            imgHeight = windowH * outsideScale;
            imgWidth = (imgHeight / realHeight) * realWidth;
        }
        else {
            if (realHeight * belowScale < windowW) {
                imgHeight = realHeight * (belowScale - 0.2);
                imgWidth = (imgHeight / realHeight) * realWidth;
            }
            else {
                imgWidth = realWidth;
                imgHeight = realHeight;
            }
        }
    }

    const outerDiv = imageViewer.parentNode;

    //设置放大图片的尺寸、偏移量并展示
    imageViewer.style.width = imgWidth + "px";
    imageViewer.style.height = imgHeight + "px";
    x = (windowW - imgWidth) * 0.5;
    y = (windowH - imgHeight) * 0.5;
    imageViewer.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    outerDiv.style.display = "block";

    // 点击蒙版及外面区域放大图片关闭
    outerDiv.onclick = () => {
        outerDiv.style.display = "none";
        initScale = 1;
        window.removeEventListener("wheel", handleStopWheel);
    };

    // 阻止事件冒泡
    imageViewer.onclick = (e) => {
        e.stopPropagation();
    };
}

function handleStopWheel(e) {
    let itemSizeChange = 1.1; //每一次滚动放大的倍数
    if (e.target.id === "imageViewer") {
        // 说明：e.dataY如果大于0则表示鼠标向下滚动，反之则向上滚动，这里设计为向上滚动为缩小，向下滚动为放大
        if (e.deltaY > 0) {
            itemSizeChange = 1 / 1.1;
        }
        let _initScale = initScale * itemSizeChange;

        // 说明：在超过或低于临界值时，虽然让 initScale 等于 maxZoom 或 minZoom，但是在后续的判断中放大图片的最终倍数并没有达到 maxZoom 或 minZoom，而是跳过。
        if (_initScale > maxZoom) {
            initScale = maxZoom;
        } else if (_initScale < minZoom) {
            initScale = minZoom;
        } else {
            initScale = _initScale;
        }
        const origin = {
            x: (itemSizeChange - 1) * imgWidth * 0.5,
            y: (itemSizeChange - 1) * imgHeight * 0.5,
        };
        // 计算偏移量
        if (_initScale < maxZoom && _initScale > minZoom) {
            x -= (itemSizeChange - 1) * (e.clientX - x) - origin.x;
            y -= (itemSizeChange - 1) * (e.clientY - y) - origin.y;
            e.target.style.transform = `translate3d(${x}px, ${y}px, 0) scale(${initScale})`;
        }
    }

    // 阻止默认事件
    e.preventDefault();
}

function imgDrag() {
    // 绑定 鼠标按下事件
    imageViewer.addEventListener("pointerdown", pointerdown);
    // 绑定 鼠标移动事件
    imageViewer.addEventListener("pointermove", pointermove);
    imageViewer.addEventListener("pointerup", function (_) {
        if (isPointerdown) {
            isPointerdown = false;
        }
    });
    imageViewer.addEventListener("pointercancel", function (_) {
        if (isPointerdown) {
            isPointerdown = false;
        }
    });
}

function pointerdown(e) {
    isPointerdown = true;
    console.log(e.pointerId)

    // 说明：Element.setPointerCapture()将特定元素指定为未来指针事件的捕获目标。指针的后续事件将以捕获元素为目标，直到捕获被释放。可以理解为：在窗口不是全屏情况下，我在拖动放大图片时即使鼠标移出可窗口之外，此时事件还是捕获在该放大图片上。
    imageViewer.setPointerCapture(e.pointerId);

    lastPointermove = {
        x: e.clientX,
        y: e.clientY,
    };
}

function pointermove(e) {
    if (isPointerdown) {
        const current1 = {
            x: e.clientX,
            y: e.clientY,
        };
        diff.x = current1.x - lastPointermove.x;
        diff.y = current1.y - lastPointermove.y;
        lastPointermove = {
            x: current1.x,
            y: current1.y,
        };
        x += diff.x;
        y += diff.y;
        imageViewer.style.transform = `translate3d(${x}px, ${y}px, 0) scale(${initScale})`;
    }
    e.preventDefault();
}