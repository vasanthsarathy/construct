(define (domain polycraft)

  (:requirements :strips :typing)
  (:types pogo_stick1 rubber1 tree_tap1 plank4 plank2 plank1 stick4 stick2 stick1 log1 tree1 crafting_table1 - object)
  (:predicates (have ?ob - object)
               (at ?ob - object)
               (inworld ?ob - object)
               (extractable ?ob1 - object ?ob2 - object)
               (holding ?ob - object)
               (nextto ?ob1 - object ?ob2 - object)
               (splittable ?ob1 - object ?ob - object)
               (craftable ?ob - object)
               (mineable ?ob1 - object ?ob2 - object)
               (used ?ob - object)
               )

  ;; Not sure move needs two params
  (:action move
    :parameters (?ob1 - object ?ob2 - object)
    :precondition (and (at ?ob1) (inworld ?ob2))
    :effect (and (not (at ?ob1)) (at ?ob2)))

  (:action craftplank
    :parameters (?p - plank4 ?l - log1)
    :precondition (and (have ?l) (not (used ?p)) (not (used ?l)))
    :effect (and (not (have ?l)) (have ?p) (used ?l)))

  (:action crafttreetap
    :parameters (?tt - tree_tap1 ?p4 - plank4 ?p1 - plank1 ?s - stick1 ?ct - crafting_table1)
    :precondition (and (have ?p4) (not (used ?p4)) (have ?p1) (not (used ?p1)) (have ?s) (not (used ?s)) (at ?ct))
    :effect (and (not (have ?p4)) (used ?p4) (not (have ?p1)) (used ?p1) (not (have ?s)) (used ?s) (have ?tt)))

  (:action split
    :parameters (?ob - object ?ob1 - object ?ob2 - object)
    :precondition (and (have ?ob) (not (used ?ob)) (not (used ?ob1)) (not (used ?ob2)) (splittable ?ob ?ob1) (splittable ?ob ?ob2))
    :effect (and (not (have ?ob)) (used ?ob) (have ?ob1) (have ?ob2)))

  (:action extractrubber
    :parameters (?tt1 - tree_tap1 ?t - tree1 ?r - rubber1)
    :precondition (and (inworld ?tt1) (not (used ?t)) (at ?t) (nextto ?tt1 ?t)(not (used ?t))  (extractable ?r ?t))
    :effect (have ?r))

  (:action craftpogostick
    :parameters (?pg - pogo_stick1 ?s - stick4 ?p - plank2 ?r - rubber1 ?ct - crafting_table1)
    :precondition (and (have ?s) (have ?p) (have ?r) (at ?ct))
    :effect (and (not (have ?s)) (not (have ?p)) (not (have ?r)) (have ?pg)))
  
  (:action placenextto
    :parameters (?ob1 - object ?ob2 - object)
    :precondition (and (holding ?ob1) (at ?ob2) (inworld ?ob2))
    :effect (and (not (holding ?ob1)) (not (have ?ob1)) (inworld ?ob1) (nextto ?ob1 ?ob2)))

  (:action pickup
    :parameters (?ob - object)
    :precondition (and (at ?ob) (inworld ?ob))
    :effect (and (have ?ob) (not (inworld ?ob))))

  (:action select
    :parameters (?ob - object)
    :precondition (and (have ?ob) (not (holding ?ob)))  
    :effect (holding ?ob))

  (:action mine
    :parameters (?material - object ?source - object)
    :precondition (and (inworld ?source) (mineable ?material ?source) (at ?source))
    :effect (and (have ?material) (used ?source) (not (inworld ?source))))

(:action craftstick
    :parameters (?s - stick4 ?p - plank2)
    :precondition (have ?p)
    :effect (and (have ?s) (not (have ?p))))



)

