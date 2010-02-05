#!/usr/bin/env python

# this line is required to get nose to run parallel tests
_multiprocess_can_split_ = True

import sys, random
from functools import partial
from itertools import starmap

import qc
from qc import *
from commons.text import *
from commons.matchers import *
forall.verbose = '-q' in sys.argv
forall = partial(forall, tries=200)

from commons import *

@forall(xs=lists(items=integers, size=(0,1000)))
def test_split_with_lambda(xs):
    xs = sorted(xs)
    m = len(xs) // 2
    (ys, zs) = splitwith(lambda x: x >= m, xs)
    assert_that(sorted(list(compact(ys, zs))), is_(equal_to(xs)))

@forall(xs=lists(items=pairs(left=integers(low=1), right=integers(low=1))))
def test_flip_smap_div(xs):
    div = lambda x, y: x / y
    rev = lambda (x, y): (y, x)
    assert_that(list(starmap(flip(div), xs)), \
                        is_(equal_to(\
                list(starmap(div,       map(rev, xs))))))

def salsa_key(x):
    return x.salsaId

class Identifiable:
    def __hash__(self):
        return hash(self.salsaId)
    def __eq__(self, other):
        return self.salsaId == other.salsaId

@forall_lazy(searchbase=
            sets(items=stubs(cls=Identifiable,
                              salsaId=strings(low=1)),
                    size=(1,3011)),
        subject=integers(low=0, high=1010))
def check_detect_using_bisect(searchbase, subject):
    searchbase = list(searchbase)
    item = searchbase[max(0, min(subject, len(searchbase) -1))]
    universe = sorted(searchbase, key=salsa_key)
    search_result = detect(cmp, item, universe, key=salsa_key)
    reason = "item (%i) mapped_to (%i)" % (universe.index(item), universe.index(search_result))
    assert_that(search_result, is_(not_none()), reason)
    assert_that(search_result.salsaId, is_(equal_to(item.salsaId)), reason)

def test_detect_using_bisect():
    [ (yield testcase) for testcase in check_detect_using_bisect() ]

def check_pluralization(singular, plural):
    assert_that(pluralize(singular), equal_to(plural))
    assert_that(singularize(plural), equal_to(singular))

def test_pluralization():
    from itertools import starmap
    # having to force strict evaluation in this was is *ugly*
    [ x for x in starmap(check_pluralization, {
        "search"      : "searches",
        "switch"      : "switches",
        "fix"         : "fixes",
        "box"         : "boxes",
        "process"     : "processes",
        "address"     : "addresses",
        "case"        : "cases",
        "stack"       : "stacks",
        "wish"        : "wishes",
        "fish"        : "fish",
    
        "category"    : "categories",
        "query"       : "queries",
        "ability"     : "abilities",
        "agency"      : "agencies",
        "movie"       : "movies",
    
        "archive"     : "archives",
    
        "index"       : "indices",
    
        "wife"        : "wives",
        "safe"        : "saves",
        "half"        : "halves",
    
        "move"        : "moves",
    
        "salesperson" : "salespeople",
        "person"      : "people",
    
        "spokesman"   : "spokesmen",
        "man"         : "men",
        "woman"       : "women",
    
        "basis"       : "bases",
        "diagnosis"   : "diagnoses",
    
        "datum"       : "data",
        "medium"      : "media",
        "analysis"    : "analyses",
    
        "node_child"  : "node_children",
        "child"       : "children",
    
        "experience"  : "experiences",
        "day"         : "days",
    
        "comment"     : "comments",
        "foobar"      : "foobars",
        "newsletter"  : "newsletters",
    
        "old_news"    : "old_news",
        "news"        : "news",
    
        "series"      : "series",
        "species"     : "species",
    
        "quiz"        : "quizzes",
    
        "perspective" : "perspectives",
    
        "ox" : "oxen",
        "photo" : "photos",
        "buffalo" : "buffaloes",
        "tomato" : "tomatoes",
        "dwarf" : "dwarves",
        "elf" : "elves",
        "information" : "information",
        "equipment" : "equipment",
        "bus" : "buses",
        "status" : "statuses",
        "mouse" : "mice",
    
        "louse" : "lice",
        "house" : "houses",
        "octopus" : "octopi",
        "virus" : "viri",
        "alias" : "aliases",
        "portfolio" : "portfolios",
    
        "vertex" : "vertices",
        "matrix" : "matrices",
    
        "axis" : "axes",
        "testis" : "testes",
        "crisis" : "crises",
    
        "rice" : "rice",
        "shoe" : "shoes",
    
        "horse" : "horses",
        "prize" : "prizes",
        "edge" : "edges"
    }.items()) ]
