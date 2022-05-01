import el from "../../util/dom.js";
import View from '../abstract.js';

export default class Bot extends View {
	static #template = `
			<fragment>
				<div>커피봇 임시</div>
			</fragment>
	`;

	constructor() {
		super();
		this.render(Bot.#template);
	}
}

customElements.define('bot-wrapper', Bot);

(() => {
	const $bot = el('<bot-wrapper class="contents" />')

	document.getElementsByClassName('bot').item(0).insertAdjacentElement('afterbegin', $bot);
})()