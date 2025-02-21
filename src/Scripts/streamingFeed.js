function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex'
}
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none'
}

function insertButtonCopy(div, index) {
    const copyButton = document.createElement('div');
    copyButton.innerHTML = `<a class="copy" href="#">📋</a>`;
    copyButton.onclick = function (event) {
        event.preventDefault(); // Prevent default anchor behavior
        const element = document.querySelector('#content-text-' + index);
        navigator.clipboard.writeText(element.innerText);
    };
    div.appendChild(copyButton);
}



function insertButtonSave(div, saveLink) {
    const saveButton = document.createElement('div');
    saveButton.innerHTML = `<a class="copy" href="${saveLink}">💾</a>`;
    div.appendChild(saveButton);
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
    componentMain.innerHTML = '';

    async function readStream() {
        showLoading();
        let index = 0
        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                hideLoading();
                break;
            }
            let chunk = decoder.decode(value, { stream: true });
            let saveLink = '';
            if (chunk.includes('_save_')) {
                saveLink = chunk.split('_save_')[1];
                chunk = chunk.split('_save_')[0];
            }
            const container = document.createElement('div');
            container.classList.add('markdown-content');
            const content = document.createElement('div');
            content.id = `content-text-${index}`
            content.innerHTML = chunk;
            container.appendChild(content);

            const buttonsContainer = document.createElement('div');
            buttonsContainer.style.display = 'flex';
            buttonsContainer.style.flexDirection = 'row';
            container.appendChild(buttonsContainer);
            insertButtonCopy(buttonsContainer, index);
            if (saveLink) {
                insertButtonSave(buttonsContainer, saveLink);
            }
            componentMain.appendChild(container);

            index++
        }
    }
    readStream();
}
export default streamingFeed;