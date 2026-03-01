# BoAT

Bogazici University Annotation Tool — a collaborative web tool for linguistic annotation and treebank management.

- **Project page:** [furkanakkurt1335.github.io/projects/boat](https://furkanakkurt1335.github.io/projects/boat)
- **Wiki:** [gitlab.com/furkan5204/boat/-/wikis](https://gitlab.com/furkan5204/boat/-/wikis/home)

## Description

A web application for collaborative dependency annotation using the [Universal Dependencies](https://universaldependencies.org/) framework. Built with Django, PostgreSQL, and Docker.

Features:
- Sentence-by-sentence annotation (CoNLL-U format)
- Multi-user collaboration with inter-annotator agreement
- Dependency graph visualization
- Treebank management (create, upload, export)
- Advanced search and filtering
- UD validation integration

## Quick Start

```bash
cd app/
docker compose -f docker-compose.dev.yml up --build -d
```

See [app/README.md](app/README.md) and the [wiki](https://gitlab.com/furkan5204/boat/-/wikis/development) for full setup instructions.

## History

- **Original desktop tool:** [boun-tabi/BoAT](https://github.com/boun-tabi/BoAT) (Qt/Python)
- **Initial web version:** [GitLab (archived)](https://gitlab.com/furkanakkurt5204/web-annotation-tool)
- **GitHub mirror:** [github.com/furkan7258/boat](https://github.com/furkan7258/boat) (archived)
