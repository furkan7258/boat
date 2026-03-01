// Auth
export interface UserRead {
	id: number;
	username: string;
	email: string;
	first_name: string;
	last_name: string;
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
	sent_id: string;
	text: string;
	order: number;
	comments: Record<string, string> | null;
}

export interface SentenceRead extends SentenceBrief {
	treebank_id: number;
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
	annotator_username: string;
	sentence_sent_id: string;
	sentence_text: string;
	sentence_comments: Record<string, string> | null;
	treebank_title: string;
}

// Search
export interface SearchResult {
	wordline_id: number;
	annotation_id: number;
	sentence_id: number;
	sent_id: string;
	text: string;
	treebank_title: string;
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
export interface DiffToken {
	id_f: string;
	form: string;
	annotations: Record<string, Record<string, string>>;
	disagreements: string[];
}
