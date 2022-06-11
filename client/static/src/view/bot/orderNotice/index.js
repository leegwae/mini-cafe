import View from "../../abstract.js";
import el from "../../../util/dom.js";
import '../userProfile';

export default class OrderNotice extends View {
	static #template = {
		error2: `
			<div>
				<p>이런, 지금은 커피 피크타임💦입니다.</p>
				<p><span>다래</span>님의 주문이 완료될때까지 <span>12</span>분 남았습니다.</p>
				<p>기다리시겠어요?
						<button class="button" data-action="wait-order-button">기다리기</button>
						<button class="button" data-action="cancel-order-button">취소하기</button>
				</p>
			</div>
		`,
		order: `
			<div>
				<p>커피 <span class="total-amount">1</span>잔 주문이 완료되었습니다!</p>
				<p>예상 대기시간은 <span>12</span>분 입니다.</p>
			</div
		`,
		completed: `
			<div>
				<p><span>다래</span>님, 맛있는 커피 <span>1</span>잔이 배달되었습니다!</p>
				<p>오늘 {{오전|오후|저녁}}도 {{활기찬|에너지 넘치는|향긋한}} 시간 보내세요!</p>
		`,
	}

	constructor() {
		super();
		this.handlers = [['click', this.onWait], ['click', this.onCancel]]
	}

	setContentByTemplateKey(key) {
		this.insertAdjacentHTML('beforeend', OrderNotice.#template[key]);
	}

	onWait(e) {
		e.preventDefault();

		const tg = e.target;
		if (tg.dataset?.action !== "wait-order-button") return;

		[...this.getElementsByTagName('button')].forEach((button) => button.disabled = true);
		/* /order(PATCH) 비동기 필요*/
	}

	onCancel(e) {
		e.preventDefault();

		const tg = e.target;
		if (tg.dataset?.action !== 'cancel-order-button') return;

		[...this.getElementsByTagName('button')].forEach((button) => button.disabled = true);
		/* /order(DELETE) 비동기 필요*/
		this.parentElement.insertAdjacentElement('beforeend', el('<user-profile></user-profile>'))
	}
}

customElements.define('order-notice', OrderNotice);
