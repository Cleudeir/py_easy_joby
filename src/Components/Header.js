class Header extends HTMLElement {
    constructor() {
        super();
        const href = this.getAttribute('href');
        const text = this.getAttribute('text');
        const onClick = this.getAttribute('onClick');
        this.innerHTML = `
            <div class="header">
                ${href ? `<a href="${href}" class="btn">
                    Back
                </a>` : ''}
                ${onClick ? `<button class="btn" onclick="${onClick}">
                    ${text}
                </button>` : ''}
            </div>
        `;
    }
}

customElements.define('my-header', Header);
export default Header;