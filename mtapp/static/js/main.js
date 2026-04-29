

function typeText(element, text, speed, callback) {
    let i = 0;

    function typing() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(typing, speed);
        } else if (callback) {
            callback();
        }
    }

    typing();
}

window.onload = function () {
    const welcome = document.getElementById("welcome-line");

    if (welcome) {
        const username = welcome.dataset.username;

        typeText(welcome, "Welcome, ", 120, function () {
            typeText(welcome, username, 120, function () {
                typeText(
                    document.getElementById("subtext-text"),
                    "Glad to see you again!",
                    80
                );
            });
        });
    } else {
        const lines = [
            "line1","line2","line3",
            "line4","line5","line6","line7"
        ];

        lines.forEach((id, index) => {
            const el = document.getElementById(id);
            if (!el) return;

            el.classList.add("fade-line");

            setTimeout(() => {
                el.classList.add("show");
            }, index * 400);
        });
    }
};

function toggleComments(postId) {
    const box = document.getElementById(`comment-box-${postId}`);

    if (!box) return;

    if (box.style.display === "none" || box.style.display === "") {
        box.style.display = "block";
    } else {
        box.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const openCommentId = params.get("open_comment");

    if (openCommentId) {
        const box = document.getElementById(`comment-box-${openCommentId}`);
        if (box) {
            box.style.display = "block";
        }
    }

    const timeElements = document.querySelectorAll(".post-time");

    timeElements.forEach(function (el) {
        const utcTime = el.dataset.time;
        if (!utcTime) return;

        const date = new Date(utcTime);

        el.textContent = date.toLocaleString([], {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            hour12: false
        });
    });
});


// textarea 自动增高
document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.querySelector('textarea[name="content"]');

    if (textarea) {
        function autoResize(el) {
            el.style.height = "auto";
            el.style.height = el.scrollHeight + "px";
        }

        textarea.addEventListener("input", function () {
            autoResize(this);
        });

        autoResize(textarea);
    }
});