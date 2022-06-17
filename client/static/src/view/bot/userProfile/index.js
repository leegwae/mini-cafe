import el from "../../../util/dom.js";
import View from "../../abstract.js";
import '../userPoint/index.js';
import '../userOrder/index.js';

export default class UserProfile extends View {
	static #template = `
		<div>
			<p><span id="user-name">다래</span>님 안녕하세요! 😀</p>
			<p>새로 주문을 하시겠어요?
					<button class="button" id="display-menu-button">메뉴보기</button>
					<button class="button" id="display-point-button">포인트보기</button>
			</p>
		</div>
	`;

	constructor() {
		super();
		const $content = el(UserProfile.#template);
		this.handlers = [['click', this.onMenuDisplay], ['click', this.onPointDisplay]]
		this.render($content);
	}

	onMenuDisplay(e) {
		e.preventDefault();

		const tg = e.target;
		if (tg.id !== 'display-menu-button') return;

		const menuEl = el('<user-order></user-order>');
		this.parentElement.insertAdjacentElement('beforeend', menuEl);
		menuEl.init();
	}

	onPointDisplay(e) {
		e.preventDefault();

		const tg = e.target;
		if (tg.id !== 'display-point-button') return;
		this.parentElement.insertAdjacentElement('beforeend', el('<user-point></user-point>'))
	}
}

customElements.define('user-profile', UserProfile);