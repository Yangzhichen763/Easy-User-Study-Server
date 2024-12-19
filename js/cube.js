
const CUBE_DELAY = 20000; // 正方体的延迟时间

function createCube() {
    const cube = document.createElement('div');
    const size = Math.random() * 50 + 30; // 随机大小
    const leftPosition = 100 + Math.random() * (window.innerWidth - 200); // 随机位置

    cube.classList.add('cube');
    cube.style.width = `${size}px`;
    cube.style.height = `${size}px`;
    cube.style.left = `${leftPosition}px`;

    // 随机旋转动画
    cube.style.animation += `, rotateAnimation ${Math.random() * 2 + 2}s infinite linear`;

    document.body.appendChild(cube);

    // 动画结束后移除元素
    setTimeout(() => {
        cube.remove();
    }, CUBE_DELAY); // 动画持续时间
}

function cubeInit() {
    createCube();
    // 每隔 20 秒创建一个小正方体
    setInterval(createCube, CUBE_DELAY);
    setTimeout(() => {
        createCube();
        setInterval(createCube, CUBE_DELAY);
    }, 3000);
    setTimeout(() => {
        createCube();
        setInterval(createCube, CUBE_DELAY);
    }, 8000);
}