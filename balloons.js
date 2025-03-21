const canvas = document.getElementById('balloonCanvas');  
const ctx = canvas.getContext('2d');  

const balloons = [];  
const balloonCount = 10; // 设置气球数量为10  

class Balloon {  
    constructor(x, y) {  
        this.x = x; // 气球的水平位置  
        this.y = y; // 气球的垂直位置  
        this.size = 20 + Math.random() * 30;  // 初始化大小，范围在20到50之间  
        this.color = this.getRandomColor(); // 随机颜色  
        this.speed = Math.random() * 2 + 1;  // 上升速度，范围在1到3之间  
    }  

    getRandomColor() {  
        const letters = '0123456789ABCDEF';  
        let color = '#';  
        for (let i = 0; i < 6; i++) {  
            color += letters[Math.floor(Math.random() * 16)];  
        }  
        return color;  
    }  

    update() {  
        this.y -= this.speed; // 气球向上移动  
        this.size += Math.sin(Date.now() * 0.001) * 0.5; // 变大变小效果  
        this.color = this.getRandomColor(); // 改变颜色  
        if (this.size < 10) this.size = 10; // 防止气球变得太小  
    }  

    draw() {  
        ctx.beginPath();  
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false); // 绘制气球圆形  
        ctx.fillStyle = this.color; // 使用气球颜色  
        ctx.fill();  
        ctx.closePath();  
    }  
}  

function init() {  
    for (let i = 0; i < balloonCount; i++) {  
        let x = Math.random() * canvas.width; // 随机x坐标  
        let y = canvas.height + Math.random() * 200; // 随机y坐标，从画布下方开始  
        balloons.push(new Balloon(x, y)); // 创建气球并添加到数组中  
    }  

    animate(); // 启动动画  
}  

function animate() {  
    ctx.clearRect(0, 0, canvas.width, canvas.height); // 清除画布  
    for (const balloon of balloons) {  
        balloon.update(); // 更新气球的属性  
        balloon.draw(); // 绘制气球  
    }  
    requestAnimationFrame(animate); // 请求下一帧动画  
}  

init(); // 初始化气球  