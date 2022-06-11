import View from '../../abstract.js'
import el from '../../../util/dom.js';

export default class UserPoint extends View {
	static #template = `
		<div class="order">
			<p>현재 포인트는 <span id="point">0</span>점입니다.</p>
		</div>
	`;

	constructor() {
		super();
		const $content = el(UserPoint.#template);
		this.render($content);
	}
}

customElements.define('user-point', UserPoint);
