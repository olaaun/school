pragma solidity ^0.4.0;

contract landmapping {

    // address of the admin team
    address admin_address = 0x123;

    // id of last created property
    int lastid = 0;

    // one geolocation
    struct coordinate {
        int longitude; // 121.549 West -> -121549
        int latitude; // 3.5 North -> +3500
    }

    struct neigh_signature {
        address neigh_address;
        bool signed;    // true iff the neighbor approved the property
    }

    struct property {
        int id;
        address owner;
        neigh_signature[] signatures;
        coordinate[] coordinates;    // list of points defining a polygon
    }

    // register of properties
    property[] properties;

    // modifier ensuring that a method is called by the admin team
    modifier isAdmin() {
        if (msg.sender != admin_address) throw;
        _;
    }

    // Send a signature
    function sign(int _propertyID, address _addr, string _sign) {
        for (uint i = 0; i < properties.length; i++) {
            if (properties[i].id == _propertyID) {
                for (uint j = 0; j < properties[i].signatures.length; j++) {
                    if(properties[i].signatures[j].neigh_address == _addr) {
                        properties[i].signatures[j].signed = true;
                        return;
                    }
                }
            }
        }
    }

    function createProperty(address _owner, int[] _longitudes, int[] _latitudes) isAdmin {
        if ( _latitudes.length != _longitudes.length || _latitudes.length < 3) return;
        property p;
        p.owner = _owner;
        p.id = lastid++;
        p.coordinates.length = _latitudes.length;
        for (uint i = 0; i < _latitudes.length; i = i++) {
            coordinate coord;
            coord.latitude = _latitudes[i];
            coord.longitude = _longitudes[i];
            p.coordinates[i] = coord;
        }
        properties.push(p);
    }

    function addNeighbors (int _id, address[] neighbors) {
        bool propertyExists = false;
        property p;
        for(uint i=0; i < properties.length; i++) {
            if (properties[i].id == _id) {
                p = properties[i];
                propertyExists = true;
                break;
            }
        }
        if (!propertyExists) return;
        for (uint j = 0; j < neighbors.length; j++) {
            p.signatures.push(neigh_signature(neighbors[j], false));
        }
    }

    // Delete Property - input: (only administration team that can delete)
    function deleteProperty(int _idToDelete) isAdmin() {
        for(uint i=0; i < properties.length; i++) {
            if (properties[i].id == _idToDelete) {
                delete properties[i];
                return;
            }
        }
    }
}
