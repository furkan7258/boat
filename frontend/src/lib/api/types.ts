// Auth
export interface UserRead {
	id: number;
	username: string;
	email: string;
	first_name: string;
	last_name: string;
	is_active: boolean;
	preferences: UserPreferences;
}

export interface UserPreferences {
	graph_preference: number;
	error_condition: boolean;
	current_columns: string[];
}

export interface Token {
	access_token: string;
	token_type: string;
}

// Treebank
export interface TreebankRead {
	id: number;
	title: string;
	language: string;
	created_at: string;
}

export interface TreebankWithProgress extends TreebankRead {
	sentence_count: number;
	annotation_count: number;
	complete_count: number;
}

// Sentence
export interface SentenceBrief {
	id: number;
	order: number;
	sent_id: string;
	text: string;
}

export interface SentenceRead extends SentenceBrief {
	treebank_id: number;
	comments: Record<string, string> | null;
	created_at: string;
}

// WordLine
export interface WordLineRead {
	id: number;
	annotation_id: number;
	id_f: string;
	form: string;
	lemma: string;
	upos: string;
	xpos: string;
	feats: string;
	head: string;
	deprel: string;
	deps: string;
	misc: string;
	feats_parsed: Record<string, string> | null;
	misc_parsed: Record<string, string> | null;
}

// Annotation
export interface AnnotationRead {
	id: number;
	sentence_id: number;
	annotator_id: number;
	status: number;
	is_template: boolean;
	is_gold: boolean;
	notes: string;
	created_at: string;
}

export interface AnnotationDetail extends AnnotationRead {
	wordlines: WordLineRead[];
	annotator_username: string | null;
	sentence_sent_id: string | null;
	sentence_text: string | null;
	sentence_comments: Record<string, string> | null;
	treebank_title: string | null;
	treebank_id: number | null;
	sentence_order: number | null;
}

// Search
export interface SearchResult {
	id: number;
	annotation_id: number;
	id_f: string;
	form: string;
	lemma: string;
	upos: string;
	xpos: string;
	feats: string;
	head: string;
	deprel: string;
	deps: string;
	misc: string;
	feats_parsed: Record<string, string> | null;
	misc_parsed: Record<string, string> | null;
	sentence_sent_id: string;
	sentence_text: string;
	treebank_title: string;
	annotator_username: string;
}

// Comment
export interface CommentRead {
	id: number;
	sentence_id: number;
	user_id: number;
	username: string;
	text: string;
	created_at: string;
}

// Diff (adjudication)
export interface DiffAnnotator {
	username: string;
	annotation_id: number;
	values: Record<string, string> | null;
}

export interface DiffToken {
	id_f: string;
	annotators: DiffAnnotator[];
	disagreements: string[];
}

export interface DiffResponse {
	sentence_id: number;
	annotator_count: number;
	token_count: number;
	disagreement_count: number;
	tokens: DiffToken[];
}

// Agreement
export interface AgreementResponse {
	treebank_id: number;
	agreement: number;
	sentences_scored: number;
}
