import math
import random
import numpy as np
import physics as ph

class FourVector:
    """ The FourVector takes a list of four numbers and interprets it as x^mu
    
    The first component is the time/energy value, components [1:] are spatial
    Four Vectors can be added, substracted and multiplied with each other.
    They can also be multiplied by numbers.
    abs_2d() returns the absolute value of the x-y directions
    abs_3d() returns the absolute value in all 3 spatial directions
    theta and phi return the angle from spherical coordinates in degrees
    angle_to gives the angle between two FourVectors' spatially in degrees
    angle_to_2d gives the angle between two FourVectors in x-y in degrees
    boost_to takes a lorentz_matrix and returns another boosted FourVector
    """
    
    def __init__(self, fourvector):
        self.vt = fourvector[0]
        self.vx = fourvector[1]
        self.vy = fourvector[2]
        self.vz = fourvector[3]
        
    def __add__(self, other):
        if isinstance(other,FourVector):
            return FourVector([self.vt + other.vt, self.vx + other.vx, 
                               self.vy + other.vy, self.vz + other.vz])
        else:
            raise TypeError("You cannot add FourVectors to non-FourVectors.")
            return None
    
    def __sub__(self, other):
        if isinstance(other,FourVector):
            return FourVector([self.vt - other.vt, self.vx - other.vx,
                               self.vy - other.vy, self.vz - other.vz])
        else:
            raise TypeError("You cannot substract non-FourVectors"
                            + " from FourVectors.")
            return None
        
    def __mul__(self, other):
        if isinstance(other, FourVector):
            return (self.vt*other.vt - self.vx*other.vx
                    - self.vy*other.vy - self.vz*other.vz)
        elif isinstance(other, int) or isinstance(other, float):
            return FourVector([other*self.vt, other*self.vx,
                         other*self.vy, other*self.vz])
        else:
            raise TypeError("You can only multiply FourVectors"+
                            " with numbers or other FourVectors.")
            return None
    
    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return FourVector([other*self.vt, other*self.vx,
                         other*self.vy, other*self.vz])
        else:
            raise TypeError("You can only multiply FourVectors"+
                            " with numbers or other FourVectors.")
            return None
    
    def __str__(self):
        return "FourVector: "+ str(self[::])
        
    def __repr__(self): 
        return str(self)
    
    def __getitem__(self, index):
        """We can index FourVector objects like any list."""
        return [self.vt, self.vx, self.vy, self.vz][index]
    
    def flipped(self):
        """Returns a FourVector flipped in its spatial components."""
        return FourVector([self.vt,-self.vx,-self.vy,-self.vz])
    
    def abs_2d(self):
        """Returns the absolute value of the x and y components."""
        return math.sqrt(self.vx**2+self.vy**2)
    
    def abs_3d(self):
        """Returns the absolute value of the spatial components."""
        return math.sqrt(self.vx**2+self.vy**2+self.vz**2)
    
    def theta(self):
        """Returns the angle theta from spherical coordinates in degrees."""
        return math.acos(self.vz/self.abs_3d())/math.pi*180
    
    def phi(self):
        """Returns the angle phi from spherical coordinates in degrees."""
        return math.atan2(self.vx,self.vy)/math.pi*180
    
    def angle_to(self, other):
        """Returns the angle between self and other (spatially) in degrees"""
        product = (self.vx*other.vx + self.vy*other.vy + self.vz*other.vz)
        if (self.vx == other.vx and self.vy == other.vy and self.vz == other.vz):
            ratio = 1.0
        else:
            ratio = product/(self.abs_3d()*other.abs_3d())
        angle = math.acos(ratio)/math.pi*180
        return angle
    
    def angle_to_2d(self, other):
        """Returns the angle between self and other in x-y in degrees"""
        product = (self.vx*other.vx + self.vy*other.vy)
        ratio = product/(self.abs_3d()*other.abs_3d())
        angle = math.acos(ratio)/math.pi*180
        return angle
    
    def boost_to(self, lorentz_matrix):
        """Returns a boosted FourVector"""
        return FourVector([
            sum([lorentz_matrix[i][j]*self[j] for j in [0,1,2,3]])
            for i in [0,1,2,3]])
    
    
class FourMomentum(FourVector):
    """FourMomentum is a FourVector.
    
    It can be constructed from a FourVector and inherits all its functions.
    All its inherited functions return FourMomentum objects, not FourVector.
    It adds the following functions:
    mass: The mass of a FourMomentum is the sqrt of its square
    gamma, beta: the relativistic gamma factor and normalised velocity
    lorentz_matrix: returns a lorentz_matrix to boost to this FM's frame
    """
    
    @classmethod
    def from_fourvector(cls, fourvector):
        """Returns a FourMomentum object with the same values as the input"""
        return cls(fourvector[::])
    
    def gamma(self):
        """Returns the relativistic gamma factor corresponding to this FM."""
        return math.sqrt(1+self.abs_3d()**2/(self.mass()**2))
    
    def beta(self):
        """Returns the relativistic velocity beta this FM corresponds to."""
        sqrt = math.sqrt(self.mass()**2+self.abs_3d()**2)
        return FourVector((1/sqrt*self)[::])
    
    def mass(self):
        """Returns the FourMomentum's mass."""
        return math.sqrt(self*self)
    
    def flipped(self):
        return FourMomentum.from_fourvector(super().flipped())
    
    def __add__(self, other):
        return FourMomentum.from_fourvector(super().__add__(other))
    
    def __sub__(self, other):
        return FourMomentum.from_fourvector(super().__sub__(other))
        
    def __mul__(self, other):
        super_result = super().__mul__(other)
        if isinstance(super_result, FourVector):
            return FourMomentum.from_fourvector(super_result)
        else:
            return super_result
    
    def __rmul__(self, other):
        super_result = super().__rmul__(other)
        if isinstance(super_result, FourVector):
            return FourMomentum.from_fourvector(super_result)
        else:
            return super_result
    
    def boost_to(self, lorentz_matrix):
        super_result = super().boost_to(lorentz_matrix)
        return FourMomentum.from_fourvector(super_result)
    
    def lorentz_matrix(self):
        """Returns the Lorentz Matrix needed to boost into this FM's frame."""
        direction = self.flipped()
        gamma = direction.gamma()
        beta = direction.beta()
        beta_abs = beta.abs_3d()
        mass = direction.mass()
        lorentz_matrix_ = [[gamma if i==0 and j==0
                          else -gamma*beta[i]*beta[j] if i==0 or j==0
                          else (gamma-1)*beta[i]*beta[j]/beta_abs**2+int(i==j)
                          for i in [0,1,2,3]] for j in [0,1,2,3]]
        return lorentz_matrix_
    
    
class Particle:
    """A Particle is described by its FourMomentum and a name/symbol.
    
    It can also optionally contain an additional FourVector for its 
    production vertex. Other optional properties may be added in the future.
    
    mass - the Particle's mass as given by its FourMomentum
    inv_mass - the invariant mass between this and another Particle
    rapidity - the Particle's rapidity
    pseudorapidity - the Particle's pseudorapidity
    boost - the Particle's boost gamma*|beta|
    decay -  Produce two decay product Particle objects from this Particle
    decay_vertex - generates the decay_vertex from the lifetime input ctau
    tracklength_to_radius - calculates length between production (0 or input)
        and given radius
    """
    def __init__(self, momentum: FourMomentum, name: str = None,
                    vertex: FourVector = None):
        self.fourmomentum = momentum
        self.name = name
        self.vertex = vertex
            
    def __str__(self):
        if self.name is not None:
            return ("Particle " + self.name + " with momentum "
                    + str(self.fourmomentum))
        else:
            return "Particle with momentum " + str(self.fourmomentum)
            
    def __repr__(self):
        return str(self)
    
    def mass(self):
        """Returns the Particle's mass as given by its FourMomentum"""
        return self.fourmomentum.mass()
    
    def inv_mass(self, other):
        """Returns the invariant mass between this and another Particle"""
        return (self.fourmomentum+other.fourmomentum).mass()

    def inv_mass_from_angle(self, other):
        """Returns the invariant mass between this and another Particle"""
        # M^2 = 2*pT1*pT2*(cosh(eta1-eta2)-cos(phi1-phi2))
        pT1 = math.sqrt(self.fourmomentum.vx*self.fourmomentum.vx + self.fourmomentum.vy*self.fourmomentum.vy)
        pT2 = math.sqrt(other.fourmomentum.vx*other.fourmomentum.vx + other.fourmomentum.vy*other.fourmomentum.vy)
        deta = self.pseudorapidity() - other.pseudorapidity()
        dphi = abs(self.fourmomentum.phi() - other.fourmomentum.phi())
        if dphi > math.pi:
            dphi -= 2*math.pi
        M2 = 2*pT1*pT2*(math.cosh(deta)-math.cos(dphi))
        return math.sqrt(M2)
    
    def rapidity(self):
        """Returns the Particle's rapidity"""
        return math.atanh(self.fourmomentum[3]/self.fourmomentum[0])
        
    def pseudorapidity(self):
        """Returns the Particle's pseudorapidity"""
        return math.atanh(self.fourmomentum[3]/self.fourmomentum.abs_3d())

    def delta_r(self, other):
        deta = self.pseudorapidity() - other.pseudorapidity()
        dphi = abs(self.fourmomentum.phi() - other.fourmomentum.phi())
        if dphi > math.pi:
            dphi -= 2*math.pi
        return math.sqrt(deta*deta + dphi*dphi)

    def boost(self):
        """Returns the Particle's boost gamma*|beta|"""
        return self.fourmomentum.abs_3d()/self.mass()
    
    def tracklength_to_radius(self, radius: float, vertex: FourVector = None):
        """The tracklength of a Particle up to a radius is calculated
        
        vertex is the Particle's production vertex. If none provided, use 
            self.vertex. If neither exists, use 0..
        This is based on assuming:
        r = abs_3d(vertex + x*mom)
        which leads to the solution:
        tracklength = sqrt(r^2-sin^2th |vertex|^2)-|vertex|*costh
        where th is the angle between vertex and mom
        If vertex outside of radius, returns 0 (no track -> no tracklength)
        """
        if vertex is None:
            if self.vertex is None:
                return radius
            else:
                vertex = self.vertex
        theta = self.fourmomentum.angle_to(vertex)
        length0 = vertex.abs_3d()
        if length0 > radius:
            return 0
        else:
            res = (math.sqrt(radius**2-math.sin(theta)**2*length0**2)
                    - math.cos(theta)*length0)
            return res
            
    def tracklength_to_rho_z(self, rho: float, z: float, 
                             vertex: FourVector = None):
        """The tracklength of a Particle up to a radius is calculated
        
        vertex is the Particle's production vertex.  If none provided, use 
            self.vertex. If neither exists, use 0..
        This is based on assuming:
        rho = abs_2d(vertex + x*mom) and z = z0 + x*pz
        which leads to two solutions for x:
        x = (sqrt(rho^2-sin^2ph |vertex|^2)-|vertex|*cosph)/pT, x = (z-z0)/pz
        where ph is the angle between vertex_T and mom_T
        If vertex outside of rho and z, returns 0 (no track -> no tracklength)
        """
        if vertex is None:
            if self.vertex is None:
                vertex = FourVector([0,0,0,0])
            else:
                vertex = self.vertex
        phi = self.fourmomentum.angle_to_2d(vertex)
        rho_0 = vertex.abs_2d()
        z_0 = vertex[3]
        if rho_0 > rho or z_0 > z:
            return 0
        else:
            pT = self.fourmomentum.abs_2d()
            if pT > 0:
                x_2d = (math.sqrt(rho**2 - rho_0**2 * math.sin(phi)**2) - rho_0 * math.cos(phi))/pT
            else:
                x_2d = 0
            pz = abs(self.fourmomentum[3])
            if pz > 0:
                x_z = (z - z_0)/pz
            else:
                x_z = 0
            if x_z != 0:
                if x_2d != 0:
                    if x_z < x_2d:
                        return self.fourmomentum.abs_3d() * x_z
                    else:
                        return self.fourmomentum.abs_3d() * x_2d
                else:
                    return self.fourmomentum.abs_3d() * x_z
            elif x_2d != 0:
                return self.fourmomentum.abs_3d() * x_2d
            else:
                return 0
                
    def decay_vertex(self, ctau: float):
        """Given a lifetime ctau this method generates a decay vertex"""
        
        decay_distance = np.random.exponential(scale=self.boost()*ctau)
        absmom = self.fourmomentum.abs_3d()
        rescaled = self.fourmomentum*(decay_distance/absmom)
        decay_vertex = FourVector(rescaled[::])
        return decay_vertex
    
    def decay(self, mass_dp: float, name_dp: str = None):
        """ Produce two decay product Particle objects from this Particle
        
        Takes the mass and optionally name of the new Particles as input
        Decays self into two identical back-to-back Particles in it rest-frame
        Boosts these back to self's original frame
        """
        th = math.acos(random.uniform(-1,1))
        ph = random.uniform(0,2*math.pi)
        my_mass = self.mass()
        reduced_mass = math.sqrt(my_mass**2/4-mass_dp**2)
        
        momentum_dp1_rest = FourMomentum([my_mass/2,
                                       reduced_mass*math.cos(ph)*math.sin(th),
                                       reduced_mass*math.sin(ph)*math.sin(th),
                                       reduced_mass*math.cos(th)])
        momentum_dp2_rest = momentum_dp1_rest.flipped()
        lorentz_matrix = self.fourmomentum.lorentz_matrix()
        momentum_dp1_lab = momentum_dp1_rest.boost_to(lorentz_matrix)
        momentum_dp2_lab = momentum_dp2_rest.boost_to(lorentz_matrix)
        if name_dp is None:
            dp1_lab = Particle(momentum_dp1_lab)
            dp2_lab = Particle(momentum_dp2_lab)
        else:
            dp1_lab = Particle(momentum_dp1_lab, name_dp)
            dp2_lab = Particle(momentum_dp2_lab, "\bar{"+name_dp+"}")
        return [dp1_lab,dp2_lab]
    
class Event:
    """ An Event contains a list of its final state Particles
    
    It can be indexed to receive a specific one.
    observable(which, [whose]) returns the property which of whose
    """
    def __init__(self, particles: [Particle]):
        self.particles = particles
        
    def __getitem__(self, index):
        return self.particles[index]
    
    def __str__(self):
        return "Event: " + str([str(part.name) for part in self.particles])
    
    def __repr__(self):
        return self.__str__()
    
    def track_from_ctau(self, i, j, radius: float, ctau: float, 
                        z: float = None, direction = "3d",
                        minimum_displacement: float = None):
        """Tracklength of Particle j if produced by i's decay with ctau
        
        i - Particle that decays and produces j
        j - Particle produced by i whose tracklength in detector is returned
        radius - radius of the detector in 3d or 2d
        ctau - lifetime of i which determines its decay vertex
        z - z coordinate of the detector if direction is 2d
        direction - "3d" for a spherical detector, "2d-z" for a cylinder,
            also determines format of return value: 3d returns single radial
            tracklength, 2d-z returns [tracklength in rho, in z]
        minimum_displacement - if j appears at smaller displacement, return 0
        """
        decay_vertex = self.particles[i].decay_vertex(ctau)
        if ((minimum_displacement is not None)
            and (decay_vertex.abs_3d()<minimum_displacement)):
            if direction == "3d":
                return 0
            elif direction == "2d-z":
                return [0,0]
        else:
            if z == 0 or z is None:
                track = self.particles[j].tracklength_to_radius(radius, decay_vertex)
            else:
                track = self.particles[j].tracklength_to_rho_z(radius, z, decay_vertex)
            mom = self.particles[j].fourmomentum
            if direction == "3d":
                return track
            elif direction == "2d-z":
                return [track * mom.abs_2d()/mom.abs_3d(), track * mom[3]/mom.abs_3d()]
        
    def observable(self, which: str, whose: [int], **kwargs):
        """Returns the property which of whose, where whose can be several.
        
        which - a property of Event or of Particle
        whose - list of indices of Particles in the Event
            The first particle calls which
            The other(s) are arguments
        kwargs - any other arguments of which, passed on as-is to which
        """
        if len(whose)==0:
            raise ValueError("There is no particle to observe anything of.")
        elif which in dir(self):
            return getattr(self, which)(*whose, **kwargs)
        else:
            ps = [self[who] for who in whose]
            if which in dir(ps[0]):
                ps[0] = getattr(ps[0],which)
            elif "." in which:
                whichlist = which.split(".")
                for part in whichlist:
                    if not part == whichlist[-1]:
                        for i in range(len(ps)):
                            ps[i] = getattr(ps[i], part)
                    else:
                        ps[0] = getattr(ps[0],part)
            else:
                raise ValueError("The particle "+str(particle)
                                 +" has no method " +str(which))
            if len(kwargs)==0:
                if len(whose)==1:
                    observable = ps[0]()
                elif len(whose)==2:
                    observable = ps[0](ps[1])
                else:
                    raise ValueError("There are more than 2 particles, "
                                +str(whose)+" , which isn't currently valid.")
            else:
                if len(whose)==1:
                    observable = ps[0](**kwargs)
                elif len(whose)==2:
                    observable = ps[0](ps[1],**kwargs)
                else:
                    raise ValueError("There are more than 2 particles, "
                                +str(whose)+" , which isn't currently valid.")
                
            return observable
    
    def counts(self, restrictions):
        """Returns whether all given restrictions apply to this event
        
        restrictions - list of tuples: (condition, which, whose, extra_args)
        condition - function with a single parameter
        which - the observable that the condition is placed on
        whose - list of Particle indices
        extra_args - additional arguments passed on as-is

        returns True if all conditions are True for self, False otherwise
        """
        for restriction in restrictions:
            if not restriction[0](self.observable(restriction[1], 
                                restriction[2], **restriction[3])):
                return False
        return True
            
                
            
class Dataset:
    """A Dataset contains a np.array of Event objects, events, and translators
    
    self.particle_dict translates from particle names (like "alp") to their 
        indices in the Event objects (like 0)
    self.observable_translator translates from short names (like "pT") to the
        internal structure of receiving an observable ("fourmomentum.abs_2d")
    self.events is the list of Event objects
    observables returns a np.array of the observable which of the particle(s)
        whose, both of which get translated with the self-owned dictionaries
        before being passed to each of the Event objects
    self.cross_section is the cross section of the dataset, default 1.0 means it won't be used
    self.int_luminosity is the luminosity, default 1.0 means it won't be used
    self.N is the total number of events
        TODO implement cross_section, int_luminosity and N better for easier use
        N should also be input in future
    """
    
    def __init__(self, events: [Event], particle_dict: dict, cross_sec = 1.0, int_lumi = 1.0):
        self.events = events
        self.particle_translator = particle_dict
        self.observable_translator = { 
            "pT": "fourmomentum.abs_2d",
            "p3": "fourmomentum.abs_3d",
            "oA": "fourmomentum.angle_to",
            "oA_2d": "fourmomentum.angle_to_2d",
            "theta": "fourmomentum.theta",
            "phi": "fourmomentum.phi",
            "y": "rapidity",
            "eta": "pseudorapidity",
            "deltaR": "delta_r"
        }
        self.cross_section = cross_sec
        self.int_luminosity = int_lumi
        self.N = len(self.events)
        
    def __str__(self):
        return f"This Dataset contains {len(self.events)} events."
    
    def __repr__(self):
        return self.__str__()

    def set_exp_weights(self, cross_sec: float, int_lumi: float, N: int):
        self.cross_section = cross_sec
        self.int_luminosity = int_lumi
        self.N = N

    def get_weighted_events(self):
        return (len(self.events)*self.cross_section*self.int_luminosity)/self.N

    def print_expected_events(self):
        print(f"This Dataset contains {(len(self.events)*self.cross_section*self.int_luminosity)/self.N} events.")
        
    def observables(self, which, whose, **kwargs):
        """Returns a np.array of the relevant observable for each Event.
        
        which is the name of the observable if it's in the dictionary
            or its direct code if it's not.
        whose is a list of names of particles in the Event, which get 
            translated into the internal indices of the Event.
        kwargs are additional arguments to be used as the argument of the
            function of the specific observable.
        """
        if which in self.observable_translator:
            which = self.observable_translator[which]
        tr_whose = [self.particle_translator[who] for who in whose]
        avg = False
        if "average" in kwargs:
            if kwargs["average"]:
                avg = True
            del kwargs["average"]
        obs_array = np.array([event.observable(which, tr_whose, **kwargs)
                         for event in self.events])
        if avg:    
            return np.average(obs_array)
        return obs_array
    
    def count_with_restrictions(self, restrictions):
        """Returns the ratio of events that hold the given restrictions
        
        restrictions - list of tuples: (condition, which, whose, extra_args)
        condition - function with a single parameter
        which - the observable that the condition is placed on
        whose - list of Particle names
        extra_args - additional arguments passed on as-is

        counts how many events follow all restrictions and gives its ratio"""
        # restrictions take the form (condition, which, [whose], extra_args)
        translated_restrictions = []
        for restriction in restrictions:
            tr_rest = []
            tr_rest.append(restriction[0])
            if restriction[1] in self.observable_translator:
                tr_rest.append(self.observable_translator[restriction[1]])
            else:
                tr_rest.append(restriction[1])
            tr_rest.append([self.particle_translator[who] for who in restriction[2]])
            if len(restriction)==4:
                tr_rest.append(restriction[3])
            else:
                tr_rest.append({})
            translated_restrictions.append(tuple(tr_rest))
        return len([1 for event in self.events if event.counts(translated_restrictions)])/len(self.events)
        
    @classmethod
    def event_selection(cls, dataset, restriction):
        # restrictions take the form (condition, which, [whose], extra_args)
        translated_restrictions = []
        tr_rest = []
        tr_rest.append(restriction[0])
        if restriction[1] in dataset.observable_translator:
            tr_rest.append(dataset.observable_translator[restriction[1]])
        else:
            tr_rest.append(restriction[1])
        tr_rest.append([dataset.particle_translator[who] for who in restriction[2]])
        if len(restriction)==4:
            tr_rest.append(restriction[3])
        else:
            tr_rest.append({})
        translated_restrictions.append(tuple(tr_rest))

        events_sel = []
        for event in dataset.events:
            if event.counts(translated_restrictions):
                events_sel.append(event)
        return cls(events_sel, dataset.particle_translator)


    @classmethod
    def from_lhe_alp(cls, filename, event_num_max=-1):
        """Reads in an .lhe file and outputs a new Dataset object from it
        
        Currently supports reading in events with ttmumu, tta or ttamumu
        in the final states. 
        If tta, produces muons from alp via alp.decay_particle function.

        Credit to Sebastian Bruggisser for the readout."""
        events = []
        event_num = 0
        case = None
        in_event = False
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('<event>'):
                    if event_num >= event_num_max and event_num_max > 0:
                        break
                    else:
                        event_num += 1
                        in_event = True
                        particle_list = []
                elif in_event:
                    if not line.startswith('</event>'):
                        line_list = line.strip('\n')
                        if len(line_list.split()) != 6:
                            particle_list.append(line_list)
                    else:
                        in_event = False
                        alp, top, antitop = None, None, None
                        muon, antimuon = None, None
                        for particle in particle_list:
                            if int(particle.split()[1]) == 1:
                                part = particle.split()
                                fourmom = FourMomentum([float(part[9]),
                                                         float(part[6]),
                                                         float(part[7]),
                                                         float(part[8])])
                                pdg_id = int(part[0])
                                if pdg_id == 9000005:
                                    alp = Particle(fourmom, "a")
                                elif pdg_id == 6:
                                    top = Particle(fourmom, "t")
                                elif pdg_id == -6:
                                    antitop = Particle(fourmom, "\bar{t}")
                                elif pdg_id == 13:
                                    muon = Particle(fourmom, "\mu")
                                elif pdg_id == -13:
                                    antimuon = Particle(fourmom, "\bar\mu")
                                else:
                                    raise InputError(f"Unexpected Particle"
                                          +f" with PDG-ID {pdg_id} found.")
                                    
                        if top is not None and antitop is not None:
                            if alp is not None:
                                if muon is not None and antimuon is not None:
                                    event = Event([alp, top, antitop, 
                                                   muon, antimuon])
                                    if case == None or case == 5:
                                        case = 5
                                    else:
                                        raise InputError("The data in this"
                                              +" .lhe file is not consistent:"
                                              +f" This is case {5} while the"
                                              +f" last was case {case}.")
                                else:
                                    if alp.mass()>2*ph.sm['mmu']:
                                        muon, antimuon = alp.decay(ph.sm['mmu'],
                                                                   "\mu")
                                        decay_particle = "muon"
                                    elif alp.mass()>2*ph.sm['me']:
                                        muon, antimuon = alp.decay(ph.sm['me'],
                                                                   "e")
                                        decay_particle = "electron"
                                    else:
                                        raise InputError("The given ALP is"
                                             +" too light to decay into muons"
                                             +f" or electrons: {alp.mass()}")
                                    event = Event([alp, top, antitop,
                                                   muon, antimuon])
                                    if case == None or case == 3:
                                        case = 3
                                    else:
                                        raise InputError("The data in this"
                                              +" .lhe file is not consistent:"
                                              +f" This is case {3} while the"
                                              +f" last was case {case}.")
                            elif muon is not None and antimuon is not None:
                                event = Event([top, antitop, muon, antimuon])
                                if case == None or case == 4:
                                    case = 4
                                else:
                                    raise InputError("The data in this"
                                          +" .lhe file is not consistent:"
                                          +f" This is case {4} while the"
                                          +f" last was case {case}.")
                            else:
                                raise InputError("The given event doesn't"
                                        +" contain the expected particles")
                        else:
                            raise InputError("The given event doesn't contain"
                                             +" the expected particles")

                        events.append(event)
                else:
                    continue
                
        if case == 5 or case == 3:
            particle_translator = {"ALP": 0, "alp": 0, "a": 0,
                                    "Top": 1, "top": 1, "t": 1, 
                                    "AntiTop": 2, "antitop": 2, "at": 2,
                                    "Muon": 3, "Muon1": 3, "muon": 3, 
                                    "mu": 3, "mu1": 3,
                                    "AntiMuon": 4, "Muon2": 4, 
                                    "antimuon": 4, "amu": 4, "mu2": 4}
        elif case == 4:
            particle_translator = {"Top": 0, "top": 0, "t": 0, 
                                    "AntiTop": 1, "antitop": 1, "at": 1,
                                    "Muon": 2, "Muon1": 2, "muon": 2, 
                                    "mu": 2, "mu1": 2,
                                    "AntiMuon": 3, "Muon2": 3, 
                                    "antimuon": 3, "amu": 3, "mu2": 3}
        else:
            raise ValueError(f"Somehow the variable case reached the value "
                    +f"{case} which is not 3, 4, or 5 and thus unexpected.")
        
        if case == 3:
            print(filename+f" read with [alp, top, antitop, {decay_particle}"
                 +f", anti{decay_particle}] in " + str(len(events))
                 +f" Events, where {decay_particle}s generated")
        elif case == 4:
            print(filename+" read with [top, antitop, muon, antimuon]"
                  +" in " + str(len(events)) + " Events.")
        elif case == 5:
            print(filename+" read with [alp, top, antitop, muon, antimuon]"
                  +" in " + str(len(events)) + " Events.")
        else:
            raise ValueError("This Part of the code should have already"
                +" raised an exception in the previous if-else statement.")
        
        return cls(events, particle_translator)

    def get_closest_muons(muons, amuons, muon_list, particles):
        index_mu = -1
        index_amu = -1
        angle_max = 0.0
        if len(muons)>0 and len(amuons)>0:
            for muon_i in muons:
                # if muon_list[muon_i].pseudorapidity() < 2.5:
                for amuon_i in amuons:
                    # if muon_list[muon_i].pseudorapidity() < 2.5:
                    angle = muon_list[muon_i].fourmomentum.angle_to(muon_list[amuon_i].fourmomentum)
                    if angle>angle_max:
                        if ((muon_list[muon_i].fourmomentum+muon_list[amuon_i].fourmomentum)*(muon_list[muon_i].fourmomentum+muon_list[amuon_i].fourmomentum)) >= 0:
                            index_mu = muon_i
                            index_amu = amuon_i
                            angle_max = angle
            # if (index_mu != muons[-1]):
            #     print(index_mu)
            # if (index_amu != amuons[-1]):
            #     print(index_amu)
            if (index_mu >= 0 and index_amu >= 0):
                particles.append(muon_list[index_mu])
                particles.append(muon_list[index_amu])
            # else:
                # print("Muon mass error, event ignored")
        return particles

    def get_closest_muons_no_charge_req(muon_list, particles):
        index_mu = -1
        index_mu2 = -1
        angle_max = 0.0
        for i in range(len(muon_list)):
            # if muon_list[muon_i].pseudorapidity() < 2.5:
            for j in range(len(muon_list)):
                if j != i:
                    # if muon_list[muon_i].pseudorapidity() < 2.5:
                    angle = muon_list[i].fourmomentum.angle_to(muon_list[j].fourmomentum)
                    if angle>angle_max:
                        if ((muon_list[i].fourmomentum+muon_list[j].fourmomentum)*(muon_list[i].fourmomentum+muon_list[j].fourmomentum)) >= 0:
                            index_mu = i
                            index_mu2 = j
                            angle_max = angle
        if (index_mu >= 0 and index_mu2 >= 0):
            particles.append(muon_list[index_mu])
            particles.append(muon_list[index_mu2])
        # else:
            # print("Muon mass error, event ignored")
        return particles

    def get_mass_error_muons(muons, amuons, muon_list, particles):
        index_mu = -1
        index_amu = -1
        angle_max = 0.0
        for i in range(len(muon_list)):
            # if muon_list[muon_i].pseudorapidity() < 2.5:
            for j in range(len(muon_list)):
                if j != i:
                    # if muon_list[muon_i].pseudorapidity() < 2.5:
                    angle = muon_list[i].fourmomentum.angle_to(muon_list[j].fourmomentum)
                    if angle>angle_max:
                        if ((muon_list[i].fourmomentum+muon_list[j].fourmomentum)*(muon_list[i].fourmomentum+muon_list[j].fourmomentum)) < 0:
                            index_mu = i
                            index_amu = j
                            angle_max = angle
        if (index_mu >= 0 and index_amu >= 0):
            particles.append(muon_list[index_mu])
            particles.append(muon_list[index_amu])
        return particles

    def get_muon_pairs(muon_pair_list, particles):
        if (len(muon_pair_list)%2 != 0):
            print("Error: unexpected number of muons in pairs: ", len(muon_pair_list))
        elif len(muon_pair_list) == 2:
            if ((muon_pair_list[0].fourmomentum+muon_pair_list[1].fourmomentum)*(muon_pair_list[0].fourmomentum+muon_pair_list[1].fourmomentum)) >= 0:
                particles.append(muon_pair_list[0])
                particles.append(muon_pair_list[1])
        else:
            i = 0
            index_pair = -1
            angle_max = 0.0
            while i < len(muon_pair_list):
                angle = muon_pair_list[i].fourmomentum.angle_to(muon_pair_list[i+1].fourmomentum)
                if angle>angle_max:
                    if ((muon_pair_list[i].fourmomentum+muon_pair_list[i+1].fourmomentum)*(muon_pair_list[i].fourmomentum+muon_pair_list[i+1].fourmomentum)) >= 0:
                        index_pair = i
                        angle_max = angle
                i += 2
            if index_pair >= 0:
                particles.append(muon_pair_list[index_pair])
                particles.append(muon_pair_list[index_pair+1])
        return particles

    @classmethod
    def from_txt_bkg(cls, filename, event_num_max=-1, charge_req=1):
        """Reads in an .txt file and outputs a new Dataset object from it
        
        This .txt file has to be of the form:
            top data | anti-top data | muon pair data | single muon data
            where data: id\t x\t y\t z\t px\t py\t pz
            and data of several such particles are appended by \t as well
            muon pairs are of the order anti-muon muon

        For now, this method chooses the first muon and antimuon, respectively
        for each Event object's muon and antimuon Particle.
        This should be reconsidered in the future. (WIP)"""
        events = []
        event_num = 0
        with open(filename, 'r') as file:
            for line in file:
                top_list, atop_list, mp_list, sm_list = line.split('|')
                
                top_list = top_list.split('\t')
                atop_list = atop_list.split('\t')
                mp_list = mp_list.split('\t')
                sm_list = sm_list.split('\t')
                
                particle_str_lists = [top_list, atop_list, mp_list, sm_list]
                particle_labels = ["t", "\bar{t}", "\mu", "\bar\mu"]
                particle_lists = []
                
                mus_no = 0
                muons = []
                amuons = []
                pmuons = []
                
                for i in range(len(particle_str_lists)):
                    p_list = particle_str_lists[i]
                    tmp_p_list = []
                    if p_list[0] == '':
                        p_list = p_list[1:]
                    if p_list[-1] == '' or p_list[-1]=='\n':
                        p_list = p_list[:-1]
                    if len(p_list)%8 != 0:
                    # if len(p_list)%9 != 0:
                        print("There is an unexpected number of data")
                    else:
                        for j in range(len(p_list)//8):
                        # for j in range(len(p_list)//9):
                            tmp_mom_list = [float(p_list[j*8+k])
                                            for k in [4,5,6,7]]
                            # tmp_mom_list = [float(p_list[j*9+k])
                            # for k in [4,5,6,7]]
                            tmp_4mom = FourMomentum(tmp_mom_list)
                            if i in [0,1]:
                                label = particle_labels[i]
                            else:
                                if p_list[j*8][0] == '-':
                                # if p_list[j*9][0] == '-':
                                    label = particle_labels[3]
                                    amuons.append(mus_no)
                                    mus_no += 1
                                else:
                                    label = particle_labels[2]
                                    muons.append(mus_no)
                                    mus_no += 1
                                if i == 2:
                                    pmuons.append(mus_no)
                            
                            tmp_v_list = [0]+[float(p_list[j*8+k])
                                              for k in [1,2,3]]
                            # tmp_v_list = [0]+[float(p_list[j*9+k])
                                            #   for k in [1,2,3]]
                            tmp_4v = FourVector(tmp_v_list)
                            if tmp_4v.abs_3d() > 10**-10:
                                tmp_p = Particle(tmp_4mom, label, tmp_4v)
                                print("FourVector used")
                            else:
                                tmp_p = Particle(tmp_4mom, label)
                            tmp_p_list.append(tmp_p)
                    particle_lists.append(tmp_p_list)
                
                final_top = particle_lists[0][-1]
                final_atop = particle_lists[1][-1]

                # Fixing an error from MadAnalysis where duplicates of the muon pairs were added
                # one muon pair [amuon, muon] is given as [amuon, muon, amuon, amuon, muons]
                if len(particle_lists[2]) == 5:
                    tmp = []
                    tmp.append(particle_lists[2][0])
                    tmp.append(particle_lists[2][1])
                    particle_lists[2] = tmp
                    amuons_tmp = [0]
                    muons_tmp = [1]
                    for i in range(3,len(amuons)):
                        amuons_tmp.append(amuons[i] - 3)
                    for i in range(2,len(muons)):
                        muons_tmp.append(muons[i]-3)
                    amuons = amuons_tmp
                    muons = muons_tmp
                if len(particle_lists[2]) == 10:
                    tmp = []
                    tmp.append(particle_lists[2][0])
                    tmp.append(particle_lists[2][1])
                    tmp.append(particle_lists[2][5])
                    tmp.append(particle_lists[2][6])
                    particle_lists[2] = tmp
                    amuons_tmp = [0,2]
                    muons_tmp = [1,3]
                    for i in range(6,len(amuons)):
                        amuons_tmp.append(amuons[i] - 6)
                    for i in range(4,len(muons)):
                        muons_tmp.append(muons[i]-6)
                    amuons = amuons_tmp
                    muons = muons_tmp
                
                particles = [final_top, final_atop]
                if mus_no>=2:
                    muon_list = particle_lists[2]+particle_lists[3]
                    if charge_req == 1:
                        particles = Dataset.get_closest_muons(muons, amuons, muon_list, particles)
                    elif charge_req == -1:
                        particles = Dataset.get_closest_muons_no_charge_req(muon_list, particles)
                    elif charge_req == 0:
                        particles = Dataset.get_mass_error_muons(muons, amuons, muon_list, particles)
                    elif charge_req == -2:
                        particles = Dataset.get_muon_pairs(particle_lists[2], particles)
                    else:
                        print("Error: invalid requirement option")
                    # index_mu = -1
                    # index_amu = -1
                    # angle_max = 0.0
                    # if len(muons)>0 and len(amuons)>0:
                    #     for muon_i in muons:
                    #         # if muon_list[muon_i].pseudorapidity() < 2.5:
                    #         for amuon_i in amuons:
                    #             # if muon_list[muon_i].pseudorapidity() < 2.5:
                    #             angle = muon_list[muon_i].fourmomentum.angle_to(muon_list[amuon_i].fourmomentum)
                    #             if angle>angle_max:
                    #                 if ((muon_list[muon_i].fourmomentum+muon_list[amuon_i].fourmomentum)*(muon_list[muon_i].fourmomentum+muon_list[amuon_i].fourmomentum)) >= 0:
                    #                     index_mu = muon_i
                    #                     index_amu = amuon_i
                    #     if (index_mu != muons[-1]):
                    #         print(index_mu)
                    #     if (index_amu != amuons[-1]):
                    #         print(index_amu)
                    #     if (index_mu >= 0 and index_amu >= 0):
                    #         particles.append(muon_list[index_mu])
                    #         particles.append(muon_list[index_amu])
                    #     else:
                    #         print("Muon mass error, event ignored")
                    if len(particles)==4:
                        events.append(Event(particles))
                        event_num += 1
                    # else:
                        # print(f"Event not included: {len(particles)} number of particles, {len(particle_lists[2])} number of muons, {len(particle_lists[3])} number of antimuons,")
                # else:
                    # print(f"Event not included: {mus_no} number of muons.")
                if event_num>=event_num_max and not event_num_max<0:
                    print(f"Too many events: {event_num}")
                    break
            
        particle_translator = {"Top": 0, "top": 0, "t": 0, 
                                "AntiTop": 1, "antitop": 1, "at": 1,
                                "Muon": 2, "Muon1": 2, "muon": 2, 
                                "mu": 2, "mu1": 2,
                                "AntiMuon": 3, "Muon2": 3, 
                                "antimuon": 3, "amu": 3, "mu2": 3}
        
        print(filename+" read with [top, antitop, muon, antimuon]"
                  +" in " + str(len(events)) + " Events.")
            
        return cls(events, particle_translator)
