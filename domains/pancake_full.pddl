(define (domain pancake)

  (:requirements :strips :typing)
  (:types   
        spw - object
        apw - object
        pw - object
        wl  - object
        vpw - object
        ly  - object
        yfl - object
        tl - object
        sl - object
        yftl  - object
        syftl - object
        pwva - object
        spwva - object
        yvaftl  - object
        syvaftl - object
        vaftyu - object
        svaftyu - object
        rmcd  - c
        rmc - c
        rc -c 
        c - object
            )
  (:predicates 
        (at ?x - object)
        (inworld ?x - object)
        (have ?x - object)
        (in ?x - object ?y - c) 
        (clean ?x - c)
    )

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;; NAVIGATION / MANIPULATION
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    (:action gofromto
    :parameters (?ob1 - object ?ob2 - object)
    :precondition (and (at ?ob1) (inworld ?ob2))
    :effect (and (not (at ?ob1)) (at ?ob2))
    )

    (:action pickup
    :parameters (?x - object)
    :precondition (and (at ?x) (inworld ?x))
    :effect (and (have ?x) (not (inworld ?x))))

    (:action putdown
    :parameters (?x - object)
    :precondition (and (have ?x))
    :effect (and (not (have ?x)) (inworld ?x)))

    (:action putin
    :parameters (?x - object ?z - c)
    :precondition (and (have ?x) (have ?z))
    :effect (and (in ?x ?z) (not (have ?x))))

    (:action takeout
    :parameters (?x - object ?z - c)
    :precondition (and (in ?x ?z) (have ?z))
    :effect (and (not (in ?x ?z)) (inworld ?x)))
 
    (:action transfer
    :parameters (?x - object ?z1 - c ?z2 - c)
    :precondition (and (have ?z1) (have ?z2) (in ?x ?z1))
    :effect (and (in ?x ?z2) (not (in ?x ?z1)))
    )

    (:action wash
    :parameters (?z - c)
    :precondition (and (have ?z))
    :effect (and (clean ?z))
    )

    ;;;;;;;;;;;;;;;;;;;;;
    ;; EGG BATTER 
    ;;;;;;;;;;;;;;;;;;;;;


    ;;  yftl (eggbatter) = yfl (yoke) + tl (eggwhite) + wl (milk) in rmc (bowl)
    ;; three inputs 
    (:action mixeggbatter1
    :parameters (?y - yftl ?x1 - yfl ?x2 - tl ?x3 - wl ?z - rmc)
    :precondition (and (have ?x1) (have ?x2) (have ?x3)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (clean ?z)) )
    )

    ;; sugar (spw variation)
    ;; four inputs 
    (:action mixeggbatter2
    :parameters (?y - syftl ?x1 - yfl ?x2 - tl ?x3 - wl ?x4 - spw ?z - rmc)
    :precondition (and (have ?x1) (have ?x2) (have ?x3) (have ?x4) (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (have ?x4)) (not (clean ?z)) )
    )

    ;;;;;;;;;;;;;;;;;;;;;;;;
    ;; DRY INGREDIENTS
    ;;;;;;;;;;;;;;;;;;;;;;;;

    
    ;; pwva (drymix) = pw (flour) + vpw (bakingpowder) + apw (salt)
    ;; 3 inputs 
    (:action mixdryingredients1
    :parameters (?y - pwva ?x1 - pw ?x2 - vpw ?x3 - apw ?z - rmc)
    :precondition (and (have ?x1) (have ?x2) (have ?x3)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (clean ?z)) )
    )

    ;; sugar variation 
    (:action mixdryingredients2
    :parameters (?y - spwva ?x1 - pw ?x2 - vpw ?x3 - apw ?x4 - spw ?z - rmc)
    :precondition (and (have ?x1) (have ?x2) (have ?x3) (have ?x4) (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (have ?x4)) (not (clean ?z)) )
    )

    ;;;;;;;;;;;;;;;;;;;;;;;
    ;; PANCAKE BATTER 
    ;;;;;;;;;;;;;;;;;;;;;;;

    ;; yvaftl (pancakebatter) = pwva (drymix) + yftl (eggbatter)
    ;; 2 input 
    (:action mixpancakebatter1
    :parameters (?y - yvaftl ?x1 - pwva ?x2 - yftl ?z - rmc)
    :precondition (and (have ?x1) (have ?x2)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (clean ?z)) )
    )

    ;; syvaftl (sweet pancakebatter)
    (:action mixpancakebatter2
    :parameters (?y - syvaftl ?x1 - pwva ?x2 - yftl ?x3 - spw ?z - rmc)
    :precondition (and (have ?x1) (have ?x2) (have ?x3)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (clean ?z)) )
    )

    (:action mixpancakebatter3
    :parameters (?y - syvaftl ?x1 - spwva ?x2 - yftl ?z - rmc)
    :precondition (and (have ?x1) (have ?x2)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (clean ?z)) )
    )

    ;; 3 inputs 
    (:action mixpancakebatter3a
    :parameters (?y - syvaftl ?x1 - spwva ?x2 - yftl ?x3 - spw ?z - rmc)
    :precondition (and (have ?x1) (have ?x2) (have ?x3)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (clean ?z)) )
    )

    (:action mixpancakebatter4
    :parameters (?y - syvaftl ?x1 - spwva ?x2 - syftl ?z - rmc)
    :precondition (and (have ?x1) (have ?x2)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (clean ?z)) )
    )

    ;; 3 inputs 
    (:action mixpancakebatter4a
    :parameters (?y - syvaftl ?x1 - spwva ?x2 - syftl ?x3 - spw ?z - rmc)
    :precondition (and (have ?x1) (have ?x2) (have ?x3)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (clean ?z)) )
    )

    (:action mixpancakebatter5
    :parameters (?y - syvaftl ?x1 - pwva ?x2 - syftl ?z - rmc)
    :precondition (and (have ?x1) (have ?x2)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (clean ?z)) )
    )

    ;; 3 inputs 
    (:action mixpancakebatter5a
    :parameters (?y - syvaftl ?x1 - pwva ?x2 - syftl ?x3 - spw ?z - rmc)
    :precondition (and (have ?x1) (have ?x2) (have ?x3)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (clean ?z)) )
    )


    ;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;; COOK PANCAKES 
    ;;;;;;;;;;;;;;;;;;;;;;;;;;

        
    ;; vaftyu (fluffy cooked pancakes) = yvaftl (pancakebatter) + yl (oil)
    (:action cookpancake1
    :parameters (?y - vaftyu ?x1 - yvaftl ?x2 - ly ?z - rmcd)
    :precondition (and (have ?x1) (have ?x2)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (clean ?z)) )
    )

    (:action cookpancake2
    :parameters (?y - svaftyu ?x1 - syvaftl ?x2 - ly ?z - rmcd)
    :precondition (and (have ?x1) (have ?x2)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (clean ?z)) )
    )

    (:action cookpancake3
    :parameters (?y - svaftyu ?x1 - yvaftl ?x2 - ly ?x3  - spw ?z - rmcd)
    :precondition (and (have ?x1) (have ?x2) (have ?x3)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (have ?x3)) (not (clean ?z)) )
    )


    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;; DRIZZLE PANCAKES 
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    (:action drizzlepancake1
    :parameters (?y - svaftyu ?x1 - vaftyu ?x2 - sl ?z - rc)
    :precondition (and (have ?x1) (have ?x2)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (clean ?z)) )
    )

    (:action drizzlepancake2
    :parameters (?y - svaftyu ?x1 - svaftyu ?x2 - sl ?z - rc)
    :precondition (and (have ?x1) (have ?x2)  (have ?z) (clean ?z))
    :effect (and (in ?y ?z) (not (have ?x1)) (not (have ?x2)) (not (clean ?z)) )
    )



)



