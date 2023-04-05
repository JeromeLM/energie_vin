# energie_vin

Project used for technical assessment. 
The aim is to create a platform listing wines sold on specialized sites with additional features.

## Detailed description
Here is the detailed description (in French) of the context of the project and what is expected :

_Un porteur de projet vous recrute en tant que premier développeur back-end dans sa jeune équipe._

_Son pitch :_

    • Concevoir une plateforme type moteur de recherche référençant les vins vendus sur des sites en ligne spécialisés.
    • Pour se démarquer de la concurrence, la fonctionnalité à forte valeur serait de fournir une évaluation de chacune des bouteilles, basée sur la moyenne des notes attribuées par les experts du domaine. 
    • Autres fonctionnalités intéressantes avec un potentiel de monétisation :
        • Un système de filtre avancé pour rechercher des vins en fonction de leurs caractéristiques.
        • Un système d’alerting où les utilisateurs peuvent sauvegarder leurs recherches et être notifiés si une bouteille nouvellement identifiée correspond.
        • L’accès à l’historisation des prix pour chaque bouteille pour comprendre la tendance.

    • Possibilité d’étendre la plateforme à d’autres types de bouteille (comme les spiritueux par exemple) si l’application est rentable.


_Quand vous lui parlez d’un MVP, le porteur de projet aimerait bien pouvoir dans un premier temps afficher les vins vendus d’un site spécialisé (wineandco ou autre), classés par la moyenne des meilleures notes, dont le prix est compris dans l’intervalle fixé par l’utilisateur._

_Vous avez rendez-vous dans quelques jours avec lui. Son souhait, est que vous puissiez mettre en place une première structure du projet avec une prémisse de développement afin que vous et les prochains développeurs, puissiez travailler dans de bonnes conditions._ 
_Vous vous engagez à fournir un premier livrable récupérable via un repo git et si besoin, tout document utile à la conception. Vous discuterez avec lui de la stratégie future : des prochains développements, de l’infrastructure et des nouveaux recrutements nécessaires à la bonne réalisation de ce projet ambitieux._

## Requirements

* docker with docker-compose

## Building and running the containers

```sh
./run.sh
```

## Testing APIs

You can use Postman to test the APIs.
Examples:
```
GET http://0.0.0.0:5005/wines
```
lists all the wines currently in the database.

```
GET http://0.0.0.0:5005/wines?sort=best_average_rating
```
lists all the wines currently in the database, sorting by the best average rating.

```
GET http://0.0.0.0:5005/wines?sort=best_average_rating&min_price=10&max_price=10.90
```
lists all the wines currently in the database, sorting by the best average rating and whose price is included in the price range.

Otherwise, you can test them by the Swagger API available here : 
```
http://0.0.0.0:5005/docs
```

## Running tests

```sh
./test.sh
```