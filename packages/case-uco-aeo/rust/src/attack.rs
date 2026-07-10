//! Adversary Engagement Ontology — attack module

use serde::Serialize;

/// An attack pattern is a common approach (set of actions) utilized by a person or organization to carry out malicious acti
#[derive(Debug, Clone, Serialize, Default)]
pub struct AttackPattern {
    pub has_objective: Vec<Objective>,
}

impl AttackPattern {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/attack/AttackPattern" }
}

/// An cyber kill chain is an ordered sequence of actions or events describing a lifecycle from some framework.
#[derive(Debug, Clone, Serialize, Default)]
pub struct CyberKillChain {
}

impl CyberKillChain {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/attack/CyberKillChain" }
}

/// A defense pattern is a common approach (set of actions) utilized by a person or organization to carry out defensive acti
#[derive(Debug, Clone, Serialize, Default)]
pub struct DefensePattern {
    pub has_objective: Vec<Objective>,
}

impl DefensePattern {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/attack/DefensePattern" }
}
