function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex'
}
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none'
}

function insertButtonCopy(div) {
    const copyButton = document.createElement('a');
    copyButton.classList.add('copy');
    copyButton.innerText = '📋';

    copyButton.onclick = function () {
        navigator.clipboard.writeText(div.innerText.split('📋')[0]);
        if (!document.getElementById('copyMessage')) {
            const message = document.createElement('span');
            message.id = 'copyMessage';
            message.classList.add('copyButton');
            message.innerText = 'Copied!';
            copyButton.after(message);
            setTimeout(() => {
                message.remove();
            }, 2000);
        }
    };
    div.appendChild(copyButton);
}
function streamingFeed(response) {
    console.log('streamingFeed');
    if (response.error !== undefined) {
        showLoading();
        return
    }
    const reader = response.data
    const decoder = new TextDecoder("utf-8");

    const componentMain = document.getElementById('documentationContent');

    componentMain.style.display = 'block';

    async function readStream() {
        showLoading();
        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                hideLoading();
                break;
            }
            const chunk = decoder.decode(value, { stream: true });
            const div = document.createElement('div');
            div.classList.add('markdown-content');
            div.innerHTML = chunk;
            insertButtonCopy(div);
            componentMain.appendChild(div);
        }
    }
    readStream();
}
export default streamingFeed;