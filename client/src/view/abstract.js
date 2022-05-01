import el from "../util/dom.js";

export default class View extends HTMLElement {
	events = new Set();
	handlers;

	constructor() {
		super();
		this.#addHandlers();
	}

	on(eventType, handler) {
		if (!this.events.has(handler)) this.events.add(handler);
		this.addEventListener(eventType, handler);

		return this;
	}

	off(eventType, handler) {
		if (this.events.has(handler)) this.removeEventListener(eventType, handler);
		
		return this;
	}
	
	dispatch(actionType, data=null) {
		const event = new CustomEvent('dispatch', { detail: { actionType, data }});
		this.dispatchEvent(event);

		return this;
	}

	render(children) {
		el(this, children instanceof Array ? children : [children]);

		return this;
	}

	#addHandlers() {
		if (this.handlers?.length) {
			this.handler.forEach(([eventType, handler]) => {
				this.on(eventType, handler);
			})
		}
	}
}