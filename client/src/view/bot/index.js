import el from "../../util/dom.js";
import View from '../abstract.js';
import './userProfile/index.js';
import './userOrder/index.js';
import './orderNotice/index.js';

export default class Bot extends View {
	static #template = `
			<fragment>
				<user-profile></user-profile>
				<user-order data-content="none"></user-order>
				<order-notice data-content="none"></order-notice>
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
