let touch_ids = {left: 0, right: 0};

function send_value(value) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/index.html");
    xhr.setRequestHeader("Content-Type", "text/plain");
    xhr.send(value);
    // console.log(value);
}

const clamp = (n, min, max) => Math.min(Math.max(n, min), max)

function down(elm, ev) {
    ctx = elm.getContext('2d')
    for(let i = 0; i < ev.changedTouches.length; i += 1) {
        const t = ev.changedTouches[i];
        if(t.identifier != touch_ids[elm.id]) {
            continue;
        }
        const y = clamp(t.pageY, 0, elm.height);
        const v = (y - elm.height * 0.5) / elm.height * 2 * 100;
        send_value(elm.id[0].toUpperCase() + v.toString());
        ctx.clearRect(0, 0, elm.width, elm.height);
        ctx.fillStyle = "#A0A0A0"
        ctx.fillRect(0, y - 5, elm.width, 10);
    }
}

function on_touch_down(ev) {
    touch_ids[this.id] = ev.changedTouches[0].identifier;
    down(this, ev);
}

function on_touch_up(ev) {
    touch_ids[this.id] = 0;
}

function on_touch_move(ev) {
    down(this, ev);
}

function init_canvas(name) {
    const canvas = document.getElementById(name);
    const ctx    = canvas.getContext('2d');

    canvas.addEventListener('touchstart', on_touch_down);
    canvas.addEventListener('touchend', on_touch_up);
    canvas.addEventListener('touchmove', on_touch_move);
}

let frame_count = 1;
let last_frame = 1;
let last_update = Date.now();
function update_monitor() {
    const monitor = document.getElementById("monitor_img");
    const src = monitor.src.substring(0, monitor.src.indexOf("?")) + "?_=" + frame_count;
    monitor.src = src;
    frame_count += 1;

    const now = Date.now();
    if(now - last_update >= 1000) {
        document.getElementById("statusline").textContent = "fps: " + (frame_count - last_frame).toString();
        last_frame = frame_count;
        last_update = now;
    }
}

function fit_canvas(canvas) {
    canvas.setAttribute("width", canvas.clientWidth);
    canvas.setAttribute("height", canvas.clientHeight);
}

function init() {
    init_canvas("left");
    init_canvas("right");

    window.onresize = function () {
        fit_canvas(document.getElementById("left"));
        fit_canvas(document.getElementById("right"));
    }

    let monitor_update_interval = 33;

    const monitor = document.getElementById("monitor_img");
    monitor.onload = function() {
        console.log("continue");
        setTimeout(update_monitor, monitor_update_interval);
    };
    monitor.onerror = function() {
        console.log("error");
        setTimeout(update_monitor, monitor_update_interval);
    };
}

document.addEventListener("DOMContentLoaded", init);
