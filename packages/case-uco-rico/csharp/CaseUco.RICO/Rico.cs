// Racketeering and Criminal Enterprise Extension — rico module
namespace CaseUco.Ext.RICO.Rico
{
    public class EnterpriseRole
    {
        public static readonly string ClassIri = "http://example.org/ontology/rico/EnterpriseRole";
        public string? RoleFunction { get; set; }
    }

    public class RacketeeringEnterprise
    {
        public static readonly string ClassIri = "http://example.org/ontology/rico/RacketeeringEnterprise";
        public string? EnterpriseType { get; set; }
    }

}