

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

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

function submitComment(postId) {
    const input = document.getElementById(`input-${postId}`);

    if (!input) {
        console.log("input not found");
        return;
    }

    const content = input.value.trim();

    console.log("submit comment", postId);
    console.log("content:", content);

    if (!content) {
        console.log("empty content");
        return;
    }


    fetch(`/api/comment/${postId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: `content=${encodeURIComponent(content)}`
    })
    .then(res => res.json())
    .then(data => {
        console.log("response:", data);

        if (data.error) {
            alert(data.error);
            return;
        }

        const box = document.getElementById(`comment-box-${postId}`);
        const form = box.querySelector(".comment-form");

        const newComment = document.createElement("div");
        newComment.className = "comment";

        newComment.innerHTML = `
            <div>${data.content}</div>
            <div class="comment-time comment-meta">
                <div>
                    <span>${new Date(data.created_at).toLocaleString([], {
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                        hour12: false
                    })}</span>
                    <span class="comment-username">${data.username}</span>
                </div>
                <form method="post" action="${data.delete_url}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                    <button type="submit" class="delete-btn">delete</button>
                </form>
            </div>
    `   ;

        box.insertBefore(newComment, form);

        input.value = "";
        box.style.display = "block";
    });
}

function deleteComment(commentId) {
    const ok = confirm("Delete this comment?");

    if (!ok) return;

    fetch(`/api/comment/${commentId}/delete/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        const comment = document.getElementById(`comment-${commentId}`);
        if (comment) {
            comment.remove();
        }
    });
}


function deletePost(postId) {
    const ok = confirm("Delete this post?");
    if (!ok) return;

    fetch(`/api/post/${postId}/delete/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        const post = document.getElementById(`post-${postId}`);
        if (post) {
            post.remove();
        }
    });
}

const translationCache = {};

function translatePost(postId) {
    const contentEl = document.getElementById(`content-${postId}`);
    const output = document.getElementById(`translation-${postId}`);

    if (!contentEl || !output) return;

    const text = contentEl.innerText.trim();

    if (!text) return;

    if (output.dataset.visible === "true") {
        output.style.display = "none";
        output.dataset.visible = "false";
        return;
    }

    if (translationCache[postId]) {
        output.innerText = translationCache[postId];
        output.style.display = "block";
        output.dataset.visible = "true";
        return;
    }

    output.innerText = "Translating...";
    output.style.display = "block";
    output.dataset.visible = "true";

    fetch("/api/translate/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: `text=${encodeURIComponent(text)}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            output.innerText = "Error: " + data.error;
            return;
        }

        translationCache[postId] = data.result;
        output.innerText = data.result;
    })
    .catch(error => {
        output.innerText = "Translation failed.";
        console.error(error);
    });
}