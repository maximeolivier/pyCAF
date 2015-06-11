## Synopsis

pyCAF est un framework d'audit de sécurité de configuration. Il a vocation à accompagner l'auditeur en lui facilitant la manipulation des données pertinentes sur lesquelles il va pouvoir baser son expertise.

## Installation

Pour simplifier l'utilisation de pyCAF, il est recommandé d'utiliser ipython.
# apt install ipython

Pour le programme s'initialise correctement et que le framework puisse être fonctionnel, il faut déposer le script ressources/00-pyCAF.py dans le rép\ertoire .ipython/profile_default/startup/ du répertoire /home de l'utilisateur. Il ne reste ensuite plus qu'à exécuter ipython avec ce fichier  (comp\ortement par défaut s'il n'existe pas d'autre code dans le répertoire startup).
$ ipython

À partir de là, les fichiers de configuration ont été chargés et le contexte d'utilisation de pyCAF (configuration et journalisation) initialisés. Il ne reste plus qu'à utiliser.

## API Reference

Les API ne sont pas encore documentées. Le travail est en cours.

## Tests

== Exemple d'import et d'analyse d'une archive ==
=== Import d'une archive extraite d'un serveur linux ===
In [1]: s = importer.Import_server_from_archive("/path/to/the/tar.bz2/archive", config)

=== Exécution d'un scénario d'analyse sur le serveur ===
In [2]: a = analyzer.AnalyzeServer(s, config)

## License

Ce code est publié sous licence GPLv3