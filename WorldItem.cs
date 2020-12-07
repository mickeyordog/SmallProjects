using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WorldItem : MonoBehaviour
{
    Rigidbody rb;
    public float speed = 1f;
    List<Vector3> waypoints = new List<Vector3>();
    List<Conveyor> waypointConveyors = new List<Conveyor>(); //must be synced with waypoints
    Vector3 previousWaypoint; //make sure this is never zero vector
    Conveyor lastTouchedConveyor;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    private void Update()
    {
        if (lastTouchedConveyor && waypoints.Count == 0)
            TryAddWaypointNext(lastTouchedConveyor);
    }

    private void FixedUpdate()
    {
        MoveToWaypoint();
    }

    private void MoveToWaypoint()
    {
        if (waypoints.Count == 0)
        {
            if (lastTouchedConveyor)
                lastTouchedConveyor.hasStationaryCargo = true;
            return;
        }
            
        float step = speed * Time.fixedDeltaTime;
        Vector3 targetPos = waypoints[0];
        rb.MovePosition(Vector3.MoveTowards(transform.position, targetPos, step));
        if ((transform.position - targetPos).sqrMagnitude < 0.01f)
        {
            previousWaypoint = targetPos;
            waypoints.RemoveAt(0);
            waypointConveyors[0].hasIncomingCargo = false;
            waypointConveyors[0].itemsStored--;
            waypointConveyors.RemoveAt(0);
        }
            
    }

    private void OnCollisionEnter(Collision collision)
    {
        CheckConveyor(collision);
    }


    private void CheckConveyor(Collision collision)
    {
        Conveyor conveyor = collision.gameObject.GetComponent<Conveyor>();
        if (conveyor == null)
            return;

        lastTouchedConveyor = conveyor;
        TryAddWaypointNext(conveyor);
    }

    private void TryAddWaypointNext(Conveyor conveyor)
    {
        if (conveyor.OutputClear())
        {
            AddWaypoint(conveyor);
        } else
        {
            conveyor.hasStationaryCargo = true;
        }
    }

    private void AddWaypoint(Conveyor c)
    {
        Vector3 result = c.GetTargetPos();
        Vector3 target = new Vector3(result.x, transform.position.y, result.z);
        if (target == previousWaypoint)
            return;

        if (waypoints.Contains(target) || c.nextInPath.hasStationaryCargo)
        {
            c.hasStationaryCargo = true;
            return;
        }
        c.nextInPath.hasIncomingCargo = true;
        waypoints.Add(target);
        waypointConveyors.Add(c.nextInPath);
        c.hasStationaryCargo = false;
    }

    private void OnDrawGizmosSelected()
    {
        foreach (Vector3 v in waypoints)
        {
            Gizmos.DrawWireSphere(v, 0.1f);
        }
    }
}

