# GPXShellExt
A module in Python 3 providing shell extensions for handling GPX tracks

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

[Description in english in the second part of this document.](###----------English----------)

### ----------Français----------

GPXShellExt est un module, écrit en Python (>= 3.8), implémentant plusieurs extensions pour l'explorateur de fichiers et le moteur d'indexation de Windows leur apportant la prise en charge des fichiers de traces de randonnée au format GPX:
  - un **gestionnaire de feuille de propriétés** affichant dans un onglet personnalisé, ainsi que dans une rubrique dédiée à la fin de la page "détails" pour ce qui est de la première trace, de la fenêtre des propriétés du fichier les métadonnées (nom, description, points de cheminement, dates et heures de début et de fin) et statistiques (durée, distance lissée, dénivelés filtrés d'élévation et d'altitude) de la ou des trace(s) incluse(s), et autorisant l'édition du nom et de la description de chaque trace;
  - un **gestionnaire de propriétés** de la première trace contenue dans le ficher, utilisable par le système pour:
    * l'indexation des métadonnées et propriétés, puis la recherche et le filtrage dans l'explorateur de fichiers au travers de requêtes AQS,
    * l'affichage des propriétés dans le panneau principal de l'explorateur de fichiers, en colonne en vue détails ou en disposition alpha à quatre lignes en vue contenu (navigation ou recherche),
    * l'affichage des propriétés et l'édition du nom et de la description dans le volet des détails de l'explorateur de fichiers;
  - un **gestionnaire de prévisualisation** assurant l'affichage de la trace sur fond cartographique et du graphique d'élévation/altitude rapportée à la distance dans le volet de prévisualisation de l'explorateur de fichiers.

Le script gère également l'enregistrement et le désenregistrement des composants COM (IShellPropSheetExt, IPropertyStore et IPreviewHandler) et du fichier XML de description de propriétés personnalisées (.propdesc) dans la base de registre, ainsi que leur association à l'extension ".gpx". S'il n'est pas exécuté avec les accès suffisants à la clé HKLM, il se relance en mode administrateur en sollicitant l'élévation de privilèges via le contrôle de compte d'utilisateur. Il est nécessaire de procéder au désenregistrement puis au réenregistrement en cas de déplacement des fichiers ou de modification des réglages de cache des tuiles ou des cartes.

Le module fait appel à deux bibliothèques du même auteur, WICPy et GPXTweaker, et ne présente aucune autre dépendance.

Pour accélérer l'affichage du fond cartographique dans le panneau de prévisualisation, il est recommandé de prétélécharger, ou tout au moins de mettre en cache, les tuiles ou cartes, en configurant en conséquence les entrées "local_pattern" (chemin d'accès du répertoire du cache des tuiles ou des cartes) et "local_store" (à "True" pour qu'elles soient conservées dans le cache au fur et à mesure de leur téléchargement) de la clé "map_handling" des réglages (voir ci-dessous). Si le répertoire du cache n'est pas un sous-répertoire du répertoire où se trouve "GPXShellExt.py", ses autorisations d'accès doivent être configurées avec un niveau obligatoire d'intégrité faible.

L'affichage des propriétés des traces dans la vue détails de l'explorateur de fichiers nécessite l'ajout des colonnes correspondantes par sélection de propriétés parmi "Nom trace", "Description trace", "Début trace", "Fin trace", "Durée trace", "Distance trace", "Dénivelé élé trace", "Dénivelé alt trace" et "Repères trace".

La recherche et le filtrage de traces dans l'explorateur de fichiers peuvent être effectuées soit en entrant directement des mots issus du nom, de la description ou des étiquettes des points de cheminement, soit au moyen de la syntaxe de requête avancée sur les champs "nom-trace", "description-trace", "début-trace", "fin-trace", "durée-trace" (en centaines de nanosecondes, c'est à dire 72e9 pour 2h), "distance-trace" (en kilomètres), "dénivelé-élé-trace" (en mètres), "dénivelé-alt-trace" (en mètres) et "repère-trace", dont quelques exemples sont donnés ci-dessous:
  - `nom-trace:(Estérel OU Maures)`;
  - `distance-trace:<=15 durée-trace:<=144e9`;
  - `début-trace:(ce mois)`;
  - `dénivelé-alt-trace:>=500 début-trace:01/01/2026..31/12/2026`;
  - `début-trace:(cette année) repère-trace:(NON "danger")`.

**Instructions de déploiement:**
  - installation:
    * option 1: créer un répertoire "GPXShellExt" dans %ProgramData% (le répertoire doit être accessible à tous les utilisateurs faute de quoi il sera indisponible pour le moteur d'indexation de Windows), et y placer les fichiers "GPXShellExt.py", depuis ce dépôt, "wic.py" et "comserver.dll", depuis le dépôt WICPy (https://github.com/PCigales/WICPy), et "GPXTweaker.py", depuis le dépôt GPXTweaker (https://github.com/PCigales/GPXTweaker),
    * option 2: exécuter, depuis une invite de commande en ligne en mode administrateur, la commande `pip install GPXShellExt`, qui installera les paquets dans le sous-répertoire "Lib\site-packages" du répertoire où se trouve Python;
  - configuration: éditer le fichier "GPXShellExt.py" en personnalisant les valeurs des entrées du dictionnaire SETTINGS:
    * smooth_range: portée, en mètres, de la fenêtre de lissage des traces,
    * ele_gain_threshold: seuil de comptabilisation, en mètres, du dénivelé d'élévation (capteur GPS),
    * alt_gain_threshold: seuil de comptabilisation, en mètres, du dénivelé d'altitude (capteur de pression),
    * slope_range: étendue, en mètres, de la fenêtre de lissage des pentes,
    * slope_max: valeur absolue maximale, en pourcentage, des pentes,
    * map_size: taille maximale, en pixels logiques (indépendants de la densité d'affichage de l'appareil), du fond cartographique,
    * map_margin: marge, en mètres, du fond cartographique par rapport à la trace,
    * map_infos: informations relatives au fournisseur et au jeu de tuiles et à la liste de matrices autorisées, ou de carte, avec indication du facteur de dézoom,
    * map_handling: paramètres de récupération des tuiles (en local ou en ligne) ou de la carte,
    * map_track_thickness: épaisseur, en pixels logiques, de la trace,
    * graph_line_thickness: épaisseur, en pixels logiques, du graphe,
    * graph_font_size: taille, en pixels logiques, de la police du graphe,
    * graph_font_fallback: police de repli, en cas d'absence d'initialisation par le système, du graphe;
  - enregistrement:
    * option 1: exécuter le script avec l'option "register", soit depuis une invite de commande en ligne, dans le répertoire où a été installée l'extension s'il ne figure pas dans la variable d'environnement PATH, `GPXShellExt register`,
    * option 2: depuis une invite de commande en ligne en mode administrateur, exécuter la commande "regsvr32 /n /i:<script_path> <dll_path>", où <script_path> et <dll_path> sont les chemins d'accès absolus respectifs à "GPXShellExt.py" et "comserver.dll", entourés de guillements doubles s'ils contiennent des espaces, soit si l'option d'installation 1 a été appliquée, `regsvr32 /n /i:"%ProgramData%\GPXShellExt\GPXShellExt.py" "%ProgramData%\GPXShellExt\comserver.dll"`;
  - désenregistrement:
    * option 1: exécuter le script avec l'option `unregister`,
    * option 2: exécuter la commande regsvr32 en ajoutant l'option `/u`.

### ----------English----------

GPXShellExt is a module, written in Python (>= 3.8), implementing several extensions for the Windows file explorer and indexing engine bringing to them support for files of hiking tracks in GPX format:
  - a **handler of properties sheet** displaying in a custom tab, as well as in a dedicated section at the end of the "details" page for the first trace, of the file properties window the metadata (name, description, waypoints, start and end dates and times) and statistics (duration, smoothed distance, filtered elevation and altitude gains) of the included track(s), and allowing the edition of the name and of the description of each track;
  - a **handler of properties** of the first track contained in the file, usable by the system for:
    * the indexing of the metadata and properties, then the search and the filtering in the file explorer through AQS queries,
    * the display of the properties in the main panel of the file explorer, in column in details view or in alpha four-line layout in content view (browsing or search),
    * the display of the properties and the edition of the name and of the description in the details pane of the file explorer;
  - a **handler of preview** ensuring the display of the track on a map and of the elevation/altitude graph relative to the distance in the preview pane of the file explorer.

The script also handles the registration and the unregistration of the COM components (IShellPropSheetExt, IPropertyStore et IPreviewHandler) and of the description of custom properties XML file (.propdesc) in the registry, as well as their association with the ".gpx" extension. If it is not executed with sufficient access to the HKLM key, it restarts in administrator mode by requesting privilege escalation via user account control. It is necessary to perform the unregistering then the reregistering in case of moving files or changing the settings of the the cache of tiles or maps.

The module uses two libraries from the same author, WICPy et GPXTweaker, and presents no other dependencies.

To speed up the display of the map in the preview pane, it is recommended to pre-download, or at the very least to cache, the tiles or maps, by setting accordingly the entries "local_pattern" (directory path of the tiles or maps cache) and "local_store" (at "True" so that they are kept in the cache as they are downloaded) of the key "map_handling" of the settings (see below). If the directory of the cache is not a subdirectory of the directory where "GPXShellExt.py" is located, its access permissions must be configured with a mandatory low integrity level.

The display of the properties of the tracks in the details view of the file explorer requires the addition of the correspondinf columns by selecting properties among "Track Name", "Track description", "Track start", "Track end", "Track duration", "Track distance", "Track ele gain", "Track alt gain" et "Track waypoints".

The searching and the filtering of the tracks in the file explorer can be performed either by directly entering words from the name, the description or the waypoints tags, either by means of the advances quesry syntax on the fields "track-name", "track-description", "track-start", "track-end", "track-duration" (in hundreds of nanoseconds, that is to say 72e9 for 2h), "track-distance" (in kilometers), "track-ele-gain" (in meters), "track-alt-gain" (in meters) and "track-waypoint", some examples of which are given below:
  - `track-name:(Estérel OR Maures)`;
  - `track-distance:<=15 track-duration:<=144e9`;
  - `track-start:(this month)`;
  - `track-alt-gain:>=500 track-start:01/01/2026..31/12/2026`;
  - `track-start:(this year) track-waypoint:(NOT "danger")`.

**Deployment instructions:**
  - installation:
    * option 1: create a directory "GPXShellExt" in %ProgramData% (the directory must be accessible to all users otherwise it will be unavailable for the Windows indexing engine), and place into it the files "GPXShellExt.py", from this repository, "wic.py" and "comserver.dll", from the repository WICPy (https://github.com/PCigales/WICPy), and "GPXTweaker.py", from the repository GPXTweaker (https://github.com/PCigales/GPXTweaker),
    * option 2: execute, from an online command prompt in administrator mode, the command `pip install GPXShellExt`, which will install the packages in the subdirectory "Lib\site-packages" of the directory where Python is located;
  - configuration: edit the file "GPXShellExt.py" by customizing the values of the entires of the dictionary SETTINGS:
    * smooth_range: range, in meters, of the smoothing window of the tracks,
    * ele_gain_threshold: accounting threshold, in meters, of the elevation gain (GPS sensor),
    * alt_gain_threshold: accounting threshold, in meters, of the altitude gain (pressure sensor),
    * slope_range: range, in meters, of the smoothing window of the slopes,
    * slope_max: maximum absolute value, in percentage, of the slopes,
    * map_size: maximum size, in logical pixels (independent of the display density of the device), of the map,
    * map_margin: margin, in meters, of the map relative to the track,
    * map_infos: information relating to the provider and to the set of tiles or maps and to the list of allowed matrices, or of card, with indication of the zoom-out factor,
    * map_handling: options of retrieval of the tiles (locally or online) or of the map,
    * map_track_thickness: thickness, in logical pixels, of the track,
    * graph_line_thickness: thickness, in logical pixels, of the graph,
    * graph_font_size: size, in logical pixels, of the font of the graph,
    * graph_font_fallback: fallback font, in case of absence of initialization by the system, of the graph;
  - registration:
    * option 1: execute the script with the option "register", that is to say, from an online command prompt, in the directory where the extension has been installed if it is not listed in the environment variable PATH, `GPXShellExt register`,
    * option 2: from an online command prompt in administrator mode, execute the command "regsvr32 /n /i:<script_path> <dll_path>", where <script_path> and <dll_path> are the respective absolute access path to "GPXShellExt.py" and "comserver.dll", enclosed in double quotes if they contain spaces, that is to say if the installation option 1 has been applied, `regsvr32 /n /i:"%ProgramData%\GPXShellExt\GPXShellExt.py" "%ProgramData%\GPXShellExt\comserver.dll"`;
  - unregistration:
    * option 1: execute the script with the option `unregister`,
    * option 2: execute the command regsvr32 by adding the option `/u`.

### ----------Illustrations----------

<img width="472" height="509" src="https://github.com/user-attachments/assets/cfcff881-8743-48bc-96ec-dd1f0775e995" />
<img width="618" height="553" src="https://github.com/user-attachments/assets/6694e70a-7077-47b6-81a5-18bac54fea2a" />
<img width="1839" height="852" src="https://github.com/user-attachments/assets/a49020e9-b749-443f-a176-b08603413e58" />


