class ButtonSubmit extends HTMLElement {
    constructor() {
        super();
        this.type = this.getAttribute('type') || 'button';
        this.text = this.getAttribute('text') || 'Click me';
        this.method = this.getAttribute('method');
        this.callback = this.getAttribute('callback');
        this.id = `button-${this.text.replace(/\s+/g, '-').toLowerCase()}`

        this.div = `
        margin-top:20px;
        `
        this.btn = `
        background-color: #007bff;
        color: white;
        padding: 10px 25px;
        text-decoration: none;
        border-radius: 5px;
        text-decoration: none;
        text-wrap: nowrap;
        
    `

        this.innerHTML = `  
        <div style="${this.div}">   
            <a type="${this.type}" style="${this.btn}" id="${this.id}">
                ${this.text}
            </a>  
        </div>     
        `;

        this.buttonElement = document.getElementById(this.id);
        this.buttonElement.addEventListener('click', (event) => {
            if (this.method === "formdata") {
                this.formData(event)
            } else if (this.method === "post") {
                this.post(event)
            }
        });
    }

    async post(event) {
        const callback = window[this.callback];
        console.log(typeof callback);
        event.preventDefault();
        const form = document.getElementById('form');
        const data = JSON.stringify(form);
        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: data
            });
            let obj = {
                status: response.status,
                data: undefined,
                error: undefined
            }
            if (response.ok) {
                try {
                    obj.data = await response.json();
                } catch (error) {
                    obj.error = error;
                }
            } else {
                obj.error = response.statusText;
            }
            if (typeof callback === 'function') {
                callback(obj);
            } else {
                alert("Error: Callback function not defined!");
            }
        } catch (error) {
            alert("An error occurred during form submission.");
        }
    }
    async formData(event) {
        const callback = window[this.callback];
        console.log(typeof callback);
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

            // Call the callback function if it exists
            if (typeof callback === 'function') {  //Check if callback is a function
                callback(obj);
            } else {
                alert("Error: Callback function not defined!");
            }
        } catch (error) {
            alert("An error occurred during form submission.");
        }
    }
}

customElements.define('my-button-submit', ButtonSubmit);

export default ButtonSubmit;