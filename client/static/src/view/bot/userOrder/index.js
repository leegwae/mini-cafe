import el, { setVisibility } from "../../../util/dom.js";
import View from "../../abstract.js";
import{ MENU } from '../const.js';
import '../orderNotice/index.js';

export default class UserOrder extends View {
	static #template = `
			<div class="order">
				<ul class="menu-list"></ul>
				<p id="total">
					총 <span class="total-amount">0</span>잔
					<button class="button" id="order-button">주문하기</button>
					<button class="button" id="cancel-button">취소하기</button>
				</p>
			</div>
		`;

	buildItem = ({ name }) => `
		<li class="menu-item" id=${name}>
			${name}
			<span class="item-amount">0</span>잔
			<button class="button plus" data-action="increase">+</button>
			<button class="button minus" data-action="decrease">-</button>
		</li>
	`;

	constructor() {
		super();
		const $content = el(UserOrder.#template);
		const $menuList = $content.getElementsByClassName('menu-list')[0]
		/* TODO: 메뉴 리스트 가져오는 비동기 작업 필요 */
		MENU.forEach((menu) => {
			$menuList.insertAdjacentHTML('beforeend', this.buildItem({ name: menu }))
		})
		this.handlers = [['click', this.onCancel], ['click', this.onOrder], ['click', this.onAmountHandle]];
		this.render($content);
	}

	onCancel = (e) => {
		e.preventDefault();

		const tg = e.target;
		if (tg.id !== 'cancel-button') return;

		[...this.getElementsByTagName('button')].forEach((button) => button.disabled = true);
		this.parentElement.insertAdjacentElement('beforeend', el('<user-profile></user-profile>'))
	}

	onOrder = (e) => {
		e.preventDefault();

		const tg = e.target;
		if (tg.id !== 'order-button') return;
		const total = Number(this.getElementsByClassName('total-amount')[0].textContent);
		if (total === 0) {
			window.alert('주문하실 메뉴를 골라주세요.');
			return;
		}
		else window.alert(`총 ${total}잔을 주문합니다.`);
	
		[...this.getElementsByClassName('button')].forEach((button) => setVisibility(button, false));
		const notice = el('<order-notice></order-notice>');
		this.parentElement.insertAdjacentElement('beforeend', notice);
		/* TODO: 주문에 따라 대기 상태 받아오는 비동기 작업 필요 */
		notice.setContentByTemplateKey('error2');
	}
	onAmountHandle = (e) => {
		e.preventDefault();

		const tg = e.target;
		if (tg.dataset.action !== 'increase' && tg.dataset.action !== 'decrease') return;
		const { action } = tg.dataset;
		const item = tg.closest('li');
		const totalElem = this.getElementsByClassName('total-amount')[0];
		const amountElem = item.getElementsByClassName('item-amount')[0];
		let total = Number(totalElem.textContent);
		let amount = Number(amountElem.textContent);

		if (action === 'increase') {
			amount += 1;
			total += 1;
		}
		else if (amount > 0) {
			amount -= 1;
			total -= 1;
		}

		amountElem.textContent = amount;
		totalElem.textContent = total;
	}
}

customElements.define('user-order', UserOrder);