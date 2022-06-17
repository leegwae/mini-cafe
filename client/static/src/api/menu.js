export const getMenu = async () => {
	const res = await fetch('/api/menu/')
	const data = await res.json();
	const { results } = data;

	return results;
}

