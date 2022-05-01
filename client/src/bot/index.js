import el from "../util/dom.js";
import View from "../view/abstract.js";

export default class bot extends View {
	static #template = `
			<fragment>
				<div>커피봇 임시</div>
			</fragment>
	`;

	constructor() {
		super();
		this.render(bot.#template);
	}
}

customElements.define('bot-wrapper', bot);

(() => {
	const $bot = el('<bot-wrapper class="contents" />')

	document.getElementsByClassName('bot').item(0).insertAdjacentElement('afterbegin', $bot);
})()