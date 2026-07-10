//! Adversary Engagement Ontology — engagement module

use serde::Serialize;

/// An Access action refers to an observed or deduced interaction between an entity and an object.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Access {
    pub name: Option<String>,
}

impl Access {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Access" }
}

/// An Alert action involves notification to some entity that some condition or event of particular interest has occurred.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Alert {
    pub name: Option<String>,
}

impl Alert {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Alert" }
}

/// An Beacon action is refer to communication between two objects where the performer is an object and the object property 
#[derive(Debug, Clone, Serialize, Default)]
pub struct Beacon {
    pub name: Option<String>,
}

impl Beacon {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Beacon" }
}

/// A Breadcrumb is a set of objects placed to be at least partially, sequentially interacted by an adversary to ellicit an 
#[derive(Debug, Clone, Serialize, Default)]
pub struct Breadcrumb {
    pub breadcrumb_target_object: Vec<UcoObject>,
    pub has_characterization: Vec<UcoObject>,
}

impl Breadcrumb {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Breadcrumb" }
}

/// A breadcrumb trail is a sequence of observed breadcrumbs where partial order of observation of breadcrumbs matter.
#[derive(Debug, Clone, Serialize, Default)]
pub struct BreadcrumbTrail {
    pub breadcrumb_target_object: Vec<UcoObject>,
    pub has_breadcrumb: Vec<Thread>,
    pub has_objective: Vec<Objective>,
}

impl BreadcrumbTrail {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/BreadcrumbTrail" }
}

/// A datasource is a grouping of characteristics unique to a specific source of data (e.g. a tool that generates event logs
#[derive(Debug, Clone, Serialize, Default)]
pub struct DataSource {
}

impl DataSource {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/DataSource" }
}

/// A datatarget is a grouping of characteristics unique to a specific target/listener that receives data (e.g. a listening 
#[derive(Debug, Clone, Serialize, Default)]
pub struct DataTarget {
}

impl DataTarget {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/DataTarget" }
}

/// A deception action is an action used for and during a deception campaign which is performed to manipulate an adversary's
#[derive(Debug, Clone, Serialize, Default)]
pub struct DeceptionAction {
}

impl DeceptionAction {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/DeceptionAction" }
}

///  A deception concept object used during a deception compaign.
#[derive(Debug, Clone, Serialize, Default)]
pub struct DeceptionObject {
    pub has_attack_surface: Vec<UcoObject>,
    pub has_characterization: Vec<UcoObject>,
    pub has_perception_characterization: Vec<UcoObject>,
}

impl DeceptionObject {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/DeceptionObject" }
}

///  A decoy is a placed object that has the perception of enough value to an adversary to pursue but contains no real value
#[derive(Debug, Clone, Serialize, Default)]
pub struct Decoy {
}

impl Decoy {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Decoy" }
}

/// A denial action is an action used for and during a deception campaign which restricts or denies an adversary access to s
#[derive(Debug, Clone, Serialize, Default)]
pub struct DenialAction {
}

impl DenialAction {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/DenialAction" }
}

/// A Deploy action involves instantiating some deception objects prior or during an operation.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Deploy {
    pub name: Option<String>,
}

impl Deploy {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Deploy" }
}

/// An Event characterizes some occurence.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Event {
    pub event_attribute: Vec<Dictionary>,
    pub event_context: Vec<UcoObject>,
    pub event_type: Vec<String>,
    pub end_time: Vec<String>,
    pub start_time: Vec<String>,
}

impl Event {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Event" }
}

///  An domain object that is created to be percieved by an adversary to have high value to pursue in an adversary engagemen
#[derive(Debug, Clone, Serialize, Default)]
pub struct HoneyObject {
}

impl HoneyObject {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/HoneyObject" }
}

/// A honey token gives an adversary direct access to a honeypot.
#[derive(Debug, Clone, Serialize, Default)]
pub struct HoneyToken {
}

impl HoneyToken {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/HoneyToken" }
}

///  A controlled environment intended to be probed, compromised or attacked by adversaries or malware.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Honeypot {
    pub honeypot_interaction_type: Vec<serde_json::Value>,
}

impl Honeypot {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Honeypot" }
}

/// A narrative is a script of all expected sequence of actions, events, entities and their interactions.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Narrative {
    pub has_objective: Vec<UcoObject>,
    pub has_storyline: Vec<UcoObject>,
}

impl Narrative {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Narrative" }
}

/// An Obfuscate action is a transformative action an entity or tool performs to some object to reduce available information
#[derive(Debug, Clone, Serialize, Default)]
pub struct Obfuscate {
    pub name: Option<String>,
}

impl Obfuscate {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Obfuscate" }
}

/// A PlannedEvent is a collection of actions, entities, interactions designated to be performed at some sequentially indexe
#[derive(Debug, Clone, Serialize, Default)]
pub struct PlannedEvent {
    pub event_context: Vec<UcoObject>,
    pub has_objective: Vec<UcoObject>,
}

impl PlannedEvent {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/PlannedEvent" }
}

/// Pocket litter describes objects placed prior or during an adversary engagement operation for the purpose of realism.
#[derive(Debug, Clone, Serialize, Default)]
pub struct PocketLitter {
    pub has_characterization: Vec<UcoObject>,
}

impl PocketLitter {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/PocketLitter" }
}

/// A Respond action is a reactive, defensive action to some adversarial detection or alert.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Respond {
    pub name: Option<String>,
}

impl Respond {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Respond" }
}

/// A Storyline is a sequence of semi-ordered planned events as an expected trajectory for a narrative.
#[derive(Debug, Clone, Serialize, Default)]
pub struct Storyline {
    pub has_event: Vec<Thread>,
}

impl Storyline {
    pub fn class_iri() -> &'static str { "https://ontology.adversaryengagement.org/ae/engagement/Storyline" }
}
