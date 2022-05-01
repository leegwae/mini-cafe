import { removeChildren, setVisibility } from "../../../util/dom.js";
import View from "../../abstract.js";

export default class UserOrder extends View {
	static #template = {
		menu: `
			<div class="order">
				<p id="total">
					총 <span class="total-amount">0</span>잔
					<button class="button" id="order-button">주문하기</button>
					<button class="button" id="cancel-button">취소하기</button>
				</p>
			</div>
		`,
		point: `
			<div class="order">
				<p>현재 포인트는 <span id="point">0</span>점입니다.</p>
			</div>`,
	};

	buildItem = ({ name }) => `
		<li id=${name}>
			${name}
			<span class="item-amount">0</span>잔
			<span class="button plus" data-action="increase">+</span>
			<span class="button minus" data-action="decrease">-</span>
		</li>
	`;

	constructor() {
		super();
		this.handlers = [['click', this.onCancel], ['click', this.onOrder], ['click', this.onAmountHandle]]
	}

	setContentByTemplateKey(key) {
		if (key === this.dataset.content) return;
		removeChildren(this);
		this.dataset.content = key;
		if (key === 'none') return;

		this.insertAdjacentHTML('beforeend', UserOrder.#template[key]);

		if (key !== 'menu') return;
		const MENU = /* 비동기 작업 필요*/ ['아메리카노', '카페라떼', '마카롱', '얼그레이 스콘'];
		MENU.forEach((menu) => {
			this.getElementsByClassName('order')[0].insertAdjacentHTML('afterbegin', this.buildItem({ name: menu }))
		})
	}
	onCancel = (e) => {
		e.preventDefault();

		const tg = e.target;
		if (tg.id !== 'cancel-button') return;
		this.setContentByTemplateKey('none')
	}
	onOrder = (e) => {
		e.preventDefault();

		const tg = e.target;
		if (tg.id !== 'order-button') return;

		const total = Number(document.getElementsByClassName('total-amount')[0].textContent);
		if (total === 0) {
			window.alert('주문하실 메뉴를 골라주세요.');
			return;
		}
		else window.alert(`총 ${total}잔을 주문합니다.`);
	
		[...tg.closest('div').getElementsByClassName('button')].forEach((button) => setVisibility(button, false));

	}
	onAmountHandle = (e) => {
		e.preventDefault();

		const tg = e.target;
		if (tg.dataset.action !== 'increase' && tg.dataset.action !== 'decrease') return;
		const { action } = tg.dataset;
		const item = tg.closest('li');
		const totalElem = document.getElementsByClassName('total-amount')[0];
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