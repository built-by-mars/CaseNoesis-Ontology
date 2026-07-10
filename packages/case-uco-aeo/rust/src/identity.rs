//! Adversary Engagement Ontology — identity module

use serde::Serialize;

///  An persona is a facticious entity created to serve a purpose in a deception operation.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Persona {
}

impl Persona {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/identity/Persona" }
}

/// The conventional reference to group of identities that are associated with some unified identity with a team objective
#[derive(Debug, Clone, Serialize, Default)]
pub struct Team {
    pub has_objective: Vec<Objective>,
}

impl Team {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/identity/Team" }
}
