"""
Tests for the lucupy idiom: Observation -> vendored minimodel Observation.

Gated on astropy (the vendored minimodel imports numpy/astropy) and on the
DEVELOPMENT-generated client (the mixins/typed scalars the converter relies on
are dev-only).
"""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from gpp_client.generated.package_environment import PACKAGE_ENVIRONMENT
from gpp_client.models.idioms import get_idiom, set_idiom, use_idiom

pytest.importorskip("astropy")
pytestmark = pytest.mark.skipif(
    PACKAGE_ENVIRONMENT != "DEVELOPMENT",
    reason="lucupy idiom relies on dev-only model enrichment",
)

from gpp_client.generated.fragments import (  # noqa: E402
    ConstraintSetDetailsElevationRange,
    ConstraintSetDetailsElevationRangeAirMass,
    GmosNorthLongSlitDetails,
    GmosNorthLongSlitDetailsCentralWavelength,
    ObservationDetailsConstraintSet,
    ObservationDetailsObservingMode,
    ObservationDetailsTargetEnvironment,
    ObservationDetailsTimingWindows,
    ObservationDetailsWorkflow,
    SiderealTargetDetailsDec,
    SiderealTargetDetailsRa,
    TargetEnvironmentDetailsAsterism,
    TargetEnvironmentDetailsAsterismSidereal,
    TimingWindowDetailsEndTimingWindowEndAfter,
    TimingWindowDetailsEndTimingWindowEndAfterAfter,
    TimingWindowDetailsEndTimingWindowEndAfterRepeat,
    TimingWindowDetailsEndTimingWindowEndAfterRepeatPeriod,
    WorkflowDetailsValue,
)
from gpp_client.generated.get_observations import (  # noqa: E402
    GetObservationsObservationsMatches,
)


@pytest.fixture(autouse=True)
def _restore_idiom():
    original = get_idiom()
    yield
    set_idiom(original)


def _build_observation(**overrides):
    """Construct an ObservationDetails-shaped observation (no validation)."""
    mc = lambda cls, **kw: cls.model_construct(**kw)  # noqa: E731

    sidereal = mc(
        TargetEnvironmentDetailsAsterismSidereal,
        ra=mc(SiderealTargetDetailsRa, hours=5.5, hms="05:30:00.000", degrees=82.5),
        dec=mc(SiderealTargetDetailsDec, degrees=-5.39, dms="-05:23:24.00"),
        epoch="J2000.000",
    )
    asterism = mc(
        TargetEnvironmentDetailsAsterism, name="Star X", sidereal=sidereal, nonsidereal=None
    )
    target_env = mc(
        ObservationDetailsTargetEnvironment, asterism=[asterism], explicit_base=None
    )

    constraint_set = mc(
        ObservationDetailsConstraintSet,
        image_quality="POINT_EIGHT",
        cloud_extinction="POINT_THREE",
        sky_background="DARK",
        water_vapor="WET",
        elevation_range=mc(
            ConstraintSetDetailsElevationRange,
            air_mass=mc(ConstraintSetDetailsElevationRangeAirMass, min=1.0, max=2.0),
            hour_angle=None,
        ),
    )

    timing_window = mc(
        ObservationDetailsTimingWindows,
        inclusion="INCLUDE",
        start_utc=datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
        end=mc(
            TimingWindowDetailsEndTimingWindowEndAfter,
            after=mc(TimingWindowDetailsEndTimingWindowEndAfterAfter, seconds=172800.0),
            repeat=mc(
                TimingWindowDetailsEndTimingWindowEndAfterRepeat,
                period=mc(
                    TimingWindowDetailsEndTimingWindowEndAfterRepeatPeriod,
                    seconds=216000.0,
                ),
                times=6,
            ),
        ),
    )

    observing_mode = mc(
        ObservationDetailsObservingMode,
        instrument="GMOS_NORTH",
        mode="GMOS_NORTH_LONG_SLIT",
        gmos_north_long_slit=mc(
            GmosNorthLongSlitDetails,
            central_wavelength=mc(
                GmosNorthLongSlitDetailsCentralWavelength,
                nanometers=500.0,
                micrometers=0.5,
            ),
        ),
    )

    workflow = mc(
        ObservationDetailsWorkflow,
        value=mc(WorkflowDetailsValue, state="READY"),
    )

    fields = dict(
        id="o-123",
        reference=SimpleNamespace(label="G-2025A-0001-Q-0002"),
        title="Demo observation",
        instrument="GMOS_NORTH",
        calibration_role=None,
        science_band="BAND1",
        workflow=workflow,
        observing_mode=observing_mode,
        constraint_set=constraint_set,
        timing_windows=[timing_window],
        target_environment=target_env,
        program=SimpleNamespace(id="p-1"),
    )
    fields.update(overrides)
    return GetObservationsObservationsMatches.model_construct(**fields)


def test_observation_to_lucupy_core_fields():
    import gpp_client.models.lucupy as mm

    obs = _build_observation()
    lo = obs.to_lucupy()

    assert isinstance(lo, mm.Observation)
    assert lo.id == mm.ObservationID("G-2025A-0001-Q-0002")
    assert lo.belongs_to == mm.ProgramID("G-2025A-0001-Q")
    assert lo.site is mm.Site.GN
    assert lo.status is mm.ObservationStatus.READY
    assert lo.band is mm.Band.BAND1
    assert lo.priority is mm.Priority.MEDIUM
    assert lo.setuptime_type is mm.SetupTimeType.FULL
    assert lo.active is True
    # GMOS long slit -> 16 min acquisition overhead.
    assert lo.acq_overhead == timedelta(minutes=16)
    assert lo.sequence == []


def test_observation_to_lucupy_target():
    obs = _build_observation()
    target = obs.to_lucupy().targets[0]

    assert target.name == "Star X"
    assert target.ra == pytest.approx(82.5)
    # Declination parsed from DMS (signed), avoiding the raw-degrees wraparound.
    assert target.dec == pytest.approx(-5.39, abs=1e-3)
    assert target.epoch == pytest.approx(2000.0)


def test_observation_to_lucupy_constraints():
    import gpp_client.models.lucupy as mm

    constraints = _build_observation().to_lucupy().constraints

    assert constraints.elevation_type is mm.ElevationType.AIRMASS
    assert constraints.elevation_min == 1.0
    assert constraints.elevation_max == 2.0
    # SkyBackground/WaterVapor map directly; CC/IQ go through percentile bins.
    assert constraints.conditions.sb == mm.SkyBackground(0.5)
    assert constraints.conditions.wv == mm.WaterVapor(1.0)
    assert constraints.conditions.cc in set(mm.CloudCover)
    assert constraints.conditions.iq in set(mm.ImageQuality)


def test_observation_to_lucupy_timing_window():
    import gpp_client.models.lucupy as mm

    window = _build_observation().to_lucupy().constraints.timing_windows[0]

    assert window.duration == timedelta(days=2)
    assert window.repeat == 6
    assert window.period == timedelta(seconds=216000)


def test_observation_to_lucupy_with_atoms():
    import gpp_client.models.lucupy as mm

    atoms = [
        SimpleNamespace(
            atom_idx=0,
            observe_class="SCIENCE",
            time_estimate=timedelta(seconds=120),
            step_index=0,
            step_count=2,
        ),
        SimpleNamespace(
            atom_idx=1,
            observe_class="ACQUISITION",  # skipped
            time_estimate=timedelta(seconds=30),
            step_index=1,
            step_count=2,
        ),
    ]
    lo = _build_observation().to_lucupy(atoms=atoms)

    assert len(lo.sequence) == 1
    assert lo.obs_class is mm.ObservationClass.SCIENCE
    assert lo.sequence[0].exec_time == timedelta(seconds=120)
    assert lo.sequence[0].obs_mode is mm.ObservationMode.LONGSLIT
    assert lo.sequence[0].resources == frozenset()


def test_lucupy_idiom_value_returns_observation():
    import gpp_client.models.lucupy as mm

    obs = _build_observation()

    assert obs.value is obs  # base idiom: the raw model
    with use_idiom("lucupy"):
        translated = obs.value
    assert isinstance(translated, mm.Observation)
    assert translated.id == mm.ObservationID("G-2025A-0001-Q-0002")


def test_leaf_value_follows_lucuma_under_lucupy_idiom():
    # A unit leaf returns its lucuma (pure-Python) value under the lucupy idiom.
    obs = _build_observation()
    window_after = obs.timing_windows[0].end.after  # TimeSpan leaf

    with use_idiom("lucupy"):
        assert window_after.value == timedelta(seconds=172800.0)
