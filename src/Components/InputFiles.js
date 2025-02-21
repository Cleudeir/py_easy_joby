class InputFiles extends HTMLElement {
    constructor() {
        super();
        this.innerHTML = `
            <label for="project_path">Select Project Directory:</label>
            <input type="file" id="project_path" name="project_path" multiple webkitdirectory directory required>
        `;
    }
}

customElements.define('my-input-files', InputFiles);
export default InputFiles;
