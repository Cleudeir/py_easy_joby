class Header extends HTMLElement {
    constructor() {
        super();
        const href = this.getAttribute('href');
        const button = this.getAttribute('button');
        const url = this.getAttribute('url');
        this.innerHTML = `
            <div class="header">
                ${href ? `<a href="${href}" class="btn">Back</a>` : ''}
                ${button ? `<a href="#" class="btn download-btn">${button}</a>` : ''}
            </div>
        `;

        // Attach event listener after element is rendered
        if (button) {
            this.querySelector('.download-btn')?.addEventListener('click', (event) => {
                event.preventDefault(); // Prevent default link behavior
                this.downloadAll(url); // Call the function dynamically
            });
        }
    }
    downloadAll(url) {
        const form = document.getElementById('form'); // Get the form
        const formData = new FormData(form);
        // check if exists files
        let check = true
        formData.forEach((value, key) => {
            console.log(value.size)
            if (value.size > 0) {
                check = false
            }
        })
        if (check) {
            return;
        }
        fetch(url, {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.blob(); // Convert response to Blob
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                console.log('url: ', url);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${url.slice(url.lastIndexOf('/') + 1)}.zip`; // File name for the download
                document.body.appendChild(a);
                a.click(); // Trigger download
                a.remove(); // Remove the link after clicking
                window.URL.revokeObjectURL(url); // Clean up memory
            })
            .catch(error => console.error('Error downloading:', error));
    }
}

customElements.define('my-header', Header);
export default Header;
