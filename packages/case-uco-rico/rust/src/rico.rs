//! Racketeering and Criminal Enterprise Extension — rico module

use serde::Serialize;

/// An enterprise role is a functional position or division-of-labor responsibility that a member or associate serves within
#[derive(Debug, Clone, Serialize, Default)]
pub struct EnterpriseRole {
    pub role_function: Option<String>,
}

impl EnterpriseRole {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/rico/EnterpriseRole" }
}

/// A racketeering enterprise is an 'enterprise' as defined in 18 U.S.C. § 1961(4) (https://www.law.cornell.edu/uscode/text/
#[derive(Debug, Clone, Serialize, Default)]
pub struct RacketeeringEnterprise {
    pub enterprise_type: Option<String>,
}

impl RacketeeringEnterprise {
    pub fn class_iri() -> &'static str { "http://example.org/ontology/rico/RacketeeringEnterprise" }
}
