# Projet de Surveillance Routière à Kolwezi

Ce projet utilise un modèle YOLOv5 pour détecter les embouteillages à partir de vidéos. Il inclut :
- Un notebook de traitement
- Une API FastAPI
- Une interface Streamlit

# Plan d'amélioration du projet

## 1. Amélioration du modèle de détection
- Tester et intégrer des modèles plus performants (YOLOv8, EfficientDet, etc.).
- Ajouter la possibilité de réentraîner le modèle sur des données locales.
- Implémenter l’augmentation de données pour améliorer la robustesse.

## 2. Pipeline de traitement vidéo
- Gérer le traitement en temps réel (streaming caméra IP/webcam).
- Ajouter la gestion de plusieurs vidéos/caméras en parallèle.
- Optimiser la vitesse d’inférence (batching, GPU, multithreading).

## 3. API & Backend
- Documenter l’API avec Swagger/OpenAPI.
- Ajouter des endpoints pour la gestion des utilisateurs et des droits d’accès.
- Implémenter la journalisation (logs) et la gestion des erreurs.

## 4. Interface utilisateur
- Créer une interface web moderne (React, Vue, ou Streamlit) pour visualiser les résultats en temps réel.
- Ajouter des dashboards analytiques (statistiques, heatmaps, graphiques).
- Permettre le téléchargement des rapports et des vidéos annotées.

## 5. Analyse avancée
- Détecter et classifier différents types de véhicules.
- Compter les véhicules, estimer la densité et détecter les infractions (franchissement de ligne, vitesse).
- Générer des alertes automatiques (mail, SMS, notifications).

## 6. Documentation & Tests
- Rédiger une documentation complète (installation, utilisation, API, architecture).
- Ajouter des tests unitaires et d’intégration pour chaque module.
- Mettre en place l’intégration continue (CI/CD).

## 7. Déploiement & Scalabilité
- Conteneuriser l’application (Docker).
- Prévoir le déploiement sur le cloud (Azure, AWS, GCP).
- Gérer la scalabilité pour traiter de grands volumes de données.

## 8. Sécurité & RGPD
- Anonymiser les données sensibles (floutage des visages, plaques).
- Sécuriser l’accès à l’API et à l’interface (authentification, HTTPS).
- Respecter la réglementation sur la vie privée.

---

Ce plan sert de feuille de route pour rendre le projet plus complet, professionnel et prêt pour une utilisation à grande échelle.
