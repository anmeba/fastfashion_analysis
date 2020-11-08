# Fast Fashion eco commitment Dataset

## Context

Entenem com a **Fast Fashion** el fenomen per el qual s’introdueixen col·leccions de roba que segueixen les últimes tendències de la moda i que han estat dissenyades i fabricades de forma accelerada i a baix cost. Empreses com _Inditex_, amb _Zara_ com a marca insígnia, abanderen aquesta filosofia. 

Aquest fenomen genera impactes ecològics com són l’alt consum de recursos naturals i productes químics a més de la generació d’abocaments i emissions. La industria de la moda es troba entre les més contaminats del món. 

## Membres de l'equip
- Ana Marrodan Badell 
- Mireia Solanich Ventura


## Descripció del dataset

El dataset proposat està composat per dos fitxer csv 
itemDimension: es recull la informació de les peces de la col·lecció de dona
CompDimension: s'obté la composició del materials i els seus percentatges

#### Contingut itemDimension
##### ItemDimension:
  - **item_code**: codi de cada article
  - **item_name**: nom de l'article
  - **item_desc**: descripció de l'article
  - **join_life**: pertany a la línia ecològica
  - **joinlife_title**: material reciclat o ecològic
  - **joinlife_desc**: descripció del material reciclat o ecològic
  - **item_price**: preu en cèntims
  
##### compDimension:
  - item_code: codi de cada article
  - part_name: zona de la peça on es descriurà la composició
  - material: material del que esta composat l'article
  - percentatge: percentatge del material que composa l'article

## Inspiració

S'ha obtingut el dataset mencionat per tal de poder dur a terme un estudi de: 
- Quin és el ús de matèries primes per a fer les diferents peces. 
- Es pretendrà analitzar quin és el consum energètic i quin és el volum de recursos naturals utilitzats en el procés de fabricació.
- Quin és el impacte econòmic.

Per a dur a terme l'estudi s'adjunta com a documentació addicional per a poder dur a terme l'estudi.



## Fonts 

Zara Sitemap: https://www.zara.com/sitemaps/sitemap-index.xml.gz
https://www.researchgate.net/publication/340635670_The_environmental_price_of_fast_fashion
https://www.contreebute.com/blog/que-es-el-fast-fashion-y-por-que-esta-haciendo-de-la-moda-un-negocio-insostenible
