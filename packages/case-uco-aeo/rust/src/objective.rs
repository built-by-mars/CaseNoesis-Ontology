//! Adversary Engagement Ontology — objective module

use serde::Serialize;

/// An objective is some particular condition or state that is desired to be achieved and toward which effort is directed: a
#[derive(Debug, Clone, Serialize, Default)]
pub struct Objective {
}

impl Objective {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/objective/Objective" }
}
