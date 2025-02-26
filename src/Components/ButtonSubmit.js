class ButtonSubmit extends HTMLElement {
    constructor() {
        super();
        this.type = this.getAttribute('type') || 'button';
        this.text = this.getAttribute('text') || 'Click me';
        this.id = `button-${this.text.replace(/\s+/g, '-').toLowerCase()}`

        this.div = `
        margin-top:20px;`
        this.btn = `
        background-color: #007bff;
        color: white;
        padding: 10px 25px;
        text-decoration: none;
        border-radius: 5px;
        text-decoration: none;
        text-wrap: nowrap;`

        this.innerHTML = `  
        <div style="${this.div}">   
            <a type="${this.type}" style="${this.btn}" id="${this.id}">
                ${this.text}
            </a>  
        </div>     
        `;

        this.buttonElement = document.getElementById(this.id);
        this.buttonElement.addEventListener('click', (event) => {
            this.getData(event)
        });
    }

    async getData(event) {
        console.log("showLoad")
        showLoading();
        event.preventDefault();
        const form = document.getElementById('form'); // Get the form
        const formData = new FormData(form);
        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData
            });
            let obj = {
                status: response.status,
                data: undefined,
                error: undefined
            }
            if (response.ok) {
                try {
                    obj.data = response.body.getReader();;
                } catch (error) {
                    obj.error = error;
                }
            } else {
                obj.error = response.statusText;
            }

            streamingFeed(obj);

        } catch (error) {
            alert("An error occurred during form submission.");
        }

    }
}

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
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
    console.log('streamingFeed', response);
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



customElements.define('my-button-submit', ButtonSubmit);
export default ButtonSubmit;