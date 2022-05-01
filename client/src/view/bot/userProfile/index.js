import el, { removeChildren, setVisibility } from "../../../util/dom.js";
import View from "../../abstract.js";

export default class UserProfile extends View {
	static #template = `
		<div>
			<p><span id="user-name">다래</span>님 안녕하세요! 😀</p>
			<p>새로 주문을 하시겠어요?
					<button class="button" data-action="toggle-content" id="display-menu-button">메뉴보기</button>
					<button class="button" data-action="toggle-content" id="display-point-button">포인트보기</button>
			</p>
		</div>
	`;

	constructor() {
		super();
		const $content = el(UserProfile.#template);
		this.handlers = [['click', this.onToggle]]
		this.render($content);
	}

	onToggle = (e) => {
		e.preventDefault();

		const tg = e.target;
		if (tg.dataset.action !== 'toggle-content') return;
		const orderElem = document.getElementsByTagName('user-order')[0];
		const newContent = tg.id.split('-')[1];

		orderElem.setContentByTemplateKey(newContent);
	}
}

customElements.define('user-profile', UserProfile);