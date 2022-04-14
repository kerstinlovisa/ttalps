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
    angle_to gives the angle between two FourVectors in degrees
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
        """Returns the angle between self and other in degrees"""
        product = (self.vx*other.vx + self.vy*other.vy + self.vz*other.vz)
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
    lorentz_matrix returns a lorentz_matrix to boost to this FM's frame
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
    
    It may in the future contain an additional FourVector for its 
    production vertex, or other properties. These will be optional.
    
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
    def __init__(self, momentum: FourMomentum, name: str = None):
        self.fourmomentum = momentum
        self.name = name
            
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
    
    def rapidity(self):
        """Returns the Particle's rapidity"""
        return math.atanh(self.fourmomentum[3]/self.fourmomentum[0])
        
    def pseudorapidity(self):
        """Returns the Particle's pseudorapidity"""
        return math.atanh(self.fourmomentum[3]/self.fourmomentum.abs_3d())
    
    def boost(self):
        """Returns the Particle's boost gamma*|beta|"""
        return self.fourmomentum.abs_3d()/self.mass()
    
    def tracklength_to_radius(self, radius: float, vertex: FourVector = None):
        """The tracklength of a Particle up to a radius is calculated
        
        vertex is the Particle's production vertex. If none provided, use 0.
        This is based on assuming:
        r = abs_3d(vertex + x*mom)
        which leads to the solution:
        tracklength = sqrt(r^2-sin^2th |vertex|^2)-|vertex|*costh
        where th is the angle between vertex and mom
        If vertex outside of radius, returns 0 (no track -> no tracklength)
        """
        if vertex == None:
            return radius
        else:
            theta = self.fourmomentum.angle_to(vertex)
            length0 = vertex.abs_3d()
            if length0 > radius:
                return 0
            else:
                res = (math.sqrt(radius**2-math.sin(theta)**2*length0**2)
                        - math.cos(theta)*length0)
                return res
        
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
                        minimum_displacement: float = None):
        """Tracklength of Particle j if produced by i's decay with ctau"""
        decay_vertex = self.particles[i].decay_vertex(ctau)
        if ((minimum_displacement is not None)
            and (decay_vertex.abs_3d()<minimum_displacement)):
            return 0
        else:
            track = self.particles[j].tracklength_to_radius(radius, decay_vertex)
            return track
        
    def observable(self, which: str, whose: [int], **kwargs):
        """Returns the property which of whose, who can be several.
        
        which can both be a property of Event as well as of a Particle
        The first particle calls the observable, the other(s) are arguments
        kwargs contain any other arguments of which that aren't Particles.
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
        """Returns whether all given restrictions apply to this event"""
        # restrictions take the form (condition, which, [whose], extra_args)
        for restriction in restrictions:
            if not restriction[0](self.observable(restriction[1], restriction[2], **restriction[3])):
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
    """
    
    def __init__(self, events: [Event], particle_dict: dict):
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
            "eta": "pseudorapidity"
        }
        
    def __str__(self):
        return f"This Dataset contains {len(self.events)} events."
    
    def __repr__(self):
        return self.__str__()
        
    def observables(self, which, whose, **kwargs):
        """Returns a np.array of the relevant observable for each Event.
        
        which is the name of the observable (if it's in the dictionary)
            or its direct code if it's not.
        whose is a list of names of particles in the Event, which get 
            translated into the internal indices of the Event.
        kwargs are additional arguments to be used as the argument of the
            function of the specific observable.
        """
        if which in self.observable_translator:
            which = self.observable_translator[which]
        tr_whose = [self.particle_translator[who] for who in whose]
        return np.array([event.observable(which, tr_whose, **kwargs)
                         for event in self.events])
    
    def count_with_restrictions(self, restrictions):
        """Returns the ratio of events that hold the given restrictions"""
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
    def from_lhe_alp(cls, filename, event_num_max=-1):
        """Reads in an .lhe file and outputs a new Dataset object from it
        
        Currently supports reading in events with ttmumu, tta or ttamumu
        in the final states. If tta, produces muons from alp.
        
        Other processes should implement extra classmethods.
        TBD: Maybe this should be a subclass?
        """
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
                 +f", anti{decay_particle}] in Events, where {decay_particle}s"
                 +" generated")
        elif case == 4:
            print(filename+" read with [top, antitop, muon, antimuon]"
                  +" in Events.")
        elif case == 5:
            print(filename+" read with [alp, top, antitop, muon, antimuon]"
                  +" in Events.")
        else:
            raise ValueError("This Part of the code should have already"
                +" raised an exception in the previous if-else statement.")
        
        return cls(events, particle_translator)