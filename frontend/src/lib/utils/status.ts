const UNTOUCHED = { label: 'Untouched', color: 'bg-muted text-muted-foreground', dot: 'bg-muted-foreground' };
const EDITED = { label: 'Edited', color: 'bg-success/10 text-success', dot: 'bg-success' };

export function getStatusConfig(status: number) {
	return status >= 2 ? EDITED : UNTOUCHED;
}
