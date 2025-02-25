class FloatingButton extends HTMLElement {
    constructor() {
        super();
        this.insertFontAwesomeLink();
        // Define the styles in JavaScript variables
        const buttonStyles = `
            position: fixed;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            border: none;
            cursor: pointer;
        `;

        const topButtonStyles = `
            ${buttonStyles}
            bottom: 20px;
            right: 20px;
            background-color: #007bff;
        `;

        const bottomButtonStyles = `
            ${buttonStyles}
            bottom: 20px;
            right: 20px;
            background-color: #28a745;
        `;

        this.innerHTML = `
        <div id="scrollToTop" style="
            ${topButtonStyles}
            display: none;
        ">      
            <a  style="${topButtonStyles}">
                <i class="fas fa-arrow-up"></i>
            </a>
        </div>
        <div id="scrollToBottom" style="
            ${bottomButtonStyles}
        ">
            <a  style="${bottomButtonStyles}">
                <i class="fas fa-arrow-down"></i>
            </a>
        </div>
        `;

    }

    connectedCallback() {

        const topButton = this.querySelector('#scrollToTop');
        const bottomButton = this.querySelector('#scrollToBottom');

        window.addEventListener('scroll', () => {
            if (window.scrollY > window.innerHeight) {
                topButton.style.display = 'block';
                bottomButton.style.display = 'none';
            } else if (window.scrollY < window.innerHeight) {
                topButton.style.display = 'none';
                bottomButton.style.display = 'block';
            }
        });

        topButton.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        bottomButton.addEventListener('click', () => {
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        });

    }

    insertFontAwesomeLink() {
        // Check if the link is already in the document to avoid duplicate inserts
        if (!document.querySelector('link[href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css"]')) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css';
            link.integrity = 'sha512-Evv84Mr4kqVGRNSgIGL/F/aIDqQb7xQ2vcrdIwxfjThSH8CSR7PBEakCr51Ck+w+/U6swU2Im1vVX0SVk9ABhg==';
            link.crossOrigin = 'anonymous';
            link.referrerPolicy = 'no-referrer';
            document.head.appendChild(link);
        }
    }
}

customElements.define('my-floating-button', FloatingButton);
export default FloatingButton;
