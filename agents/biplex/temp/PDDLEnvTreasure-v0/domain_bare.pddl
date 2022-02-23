(define (domain treasure)

  (:requirements :strips :typing)
  (:types p q r b s k t - object)
  (:predicates (at ?ob - object)
               (inworld ?ob - object)
               (opened ?x - b)
               (have ?ob - object)
               (ready ?ob - object)
               (in ?ob - object ?x - b)
               )

  (:action move
    :parameters (?ob1 - object ?ob2 - object)
    :precondition (and (at ?ob1) (inworld ?ob2))
    :effect (and (not (at ?ob1)) (at ?ob2)))

    (:action pickup
    :parameters (?ob - object)
    :precondition (and (at ?ob) (inworld ?ob))
    :effect (and (have ?ob) (not (inworld ?ob))))

    (:action open 
    :parameters (?x - b ?y - k)
    :precondition (and (at ?x) (have ?y))
    :effect (and (opened ?x)))

    (:action takeout 
    :parameters (?x - object ?y - b)
    :precondition (and (in ?x ?y) (at ?y) (opened ?y))
    :effect (and (inworld ?x)))
)
