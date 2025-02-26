class ButtonSubmit extends HTMLElement {
    constructor() {
        super();
        this.type = this.getAttribute('type') || 'button';
        this.text = this.getAttribute('text') || 'Click me';
        this.id = `button-${this.text.replace(/\s+/g, '-').toLowerCase()}`;
        this.onlyName = this.hasAttribute('onlyName');

        this.div = `
        margin-top:20px;`;
        this.btn = `
        background-color: #007bff;
        color: white;
        padding: 10px 25px;
        text-decoration: none;
        border-radius: 5px;
        text-wrap: nowrap;`;

        this.innerHTML = `  
        <div style="${this.div}">   
            <a type="${this.type}" style="${this.btn}" id="${this.id}">
                ${this.text}
            </a>  
        </div>     
        `;

        this.buttonElement = document.getElementById(this.id);
        this.buttonElement.addEventListener('click', (event) => {
            showLoading();
            hiddenContent();
            this.getData(event);
        });
    }

    async getData(event) {
        event.preventDefault();
        const form = document.getElementById('form');
        const formData = new FormData();

        for (const entry of new FormData(form).entries()) {
            console.log(entry[1]);
            if (this.onlyName && entry[1] instanceof File) {
                formData.append(entry[0], entry[1].webkitRelativePath);
            } else {
                formData.append(entry[0], entry[1]);
            }
        }
        JSON.stringify(formData, null, 2);

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData
            });
            let obj = {
                status: response.status,
                data: undefined,
                error: undefined
            };
            if (response.ok) {
                try {
                    obj.data = response.body.getReader();
                } catch (error) {
                    obj.error = error;
                }
            } else {
                obj.error = response.statusText;
            }

            streamingFeed(obj);

        } catch (error) {
            alert(error);
        }
    }
}

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function hiddenContent() {
    const componentMain = document.getElementById('documentationContent');
    componentMain.style.display = 'none';
    componentMain.innerHTML = '';
}
function showContent() {
    const componentMain = document.getElementById('documentationContent');
    componentMain.style.display = 'block';
    componentMain.innerHTML = '';
    return componentMain;
}

function streamingFeed(response) {
    console.log('streamingFeed', response);
    if (response.error !== undefined) {
        showLoading();
        return;
    }
    const reader = response.data;
    const decoder = new TextDecoder("utf-8");
    const componentMain = showContent();

    async function readStream() {
        showLoading();
        let index = 0;
        let processing = false;
        while (true) {
            if (processing) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            processing = true;
            const { done, value } = await reader.read();
            if (done) {
                hideLoading();
                break;
            }
            let chunk = decoder.decode(value, { stream: true });

            const container = document.createElement('div');
            container.classList.add('markdown-content');
            // create content
            const content = document.createElement('div');
            content.id = `content-text-${index}`;
            content.innerHTML = chunk;
            // add content
            container.appendChild(content);

            const buttonsContainer = document.createElement('div');
            buttonsContainer.style.display = 'flex';
            buttonsContainer.style.flexDirection = 'row';
            container.appendChild(buttonsContainer);

            const copyButton = document.createElement('div');
            copyButton.innerHTML = `<a class="copy" href="#">📋</a>`;
            copyButton.onclick = function (event) {
                event.preventDefault();
                const element = document.querySelector('#content-text-' + index);
                navigator.clipboard.writeText(element.innerText);
            };
            container.appendChild(copyButton);

            componentMain.appendChild(container);

            index++;
        }
    }
    readStream();
}

customElements.define('my-button-submit', ButtonSubmit);
export default ButtonSubmit;
